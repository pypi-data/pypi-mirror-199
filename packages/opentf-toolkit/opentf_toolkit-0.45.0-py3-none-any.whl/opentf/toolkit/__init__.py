# Copyright (c) 2021-2023 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A toolkit for creating OpenTestFactory plugins."""

from typing import Any, Callable, Dict, Optional

import inspect
import os
import sys

from flask import request, g

import yaml

from opentf.commons import (
    make_app,
    run_app,
    subscribe,
    unsubscribe,
    EXECUTIONCOMMAND,
    PROVIDERCOMMAND,
    PROVIDERCONFIG,
    GENERATORCOMMAND,
    SERVICECONFIG,
    validate_schema,
    make_status_response,
)
from opentf.toolkit import core


########################################################################

SUBSCRIPTION_KEY = '__subscription uuid__'
MANIFEST_KEY = '__manifest key__'
KIND_KEY = '__kind key__'
INPUTS_KEY = '__inputs key__'

Handler = Callable[[Dict[str, Any]], Any]

########################################################################


def _ensure_inputs_match(
    plugin, labels: Dict[str, str], inputs: Dict[str, Any]
) -> None:
    """Check inputs.

    Fills missing optional inputs with their default values if
    specified.

    # Raised exceptions

    A _core.ExecutionError_ is raised if a required entry is missing,
    or if an unexpected entry is found.
    """
    cache = plugin.config['CONTEXT'][INPUTS_KEY]
    prefix = labels.get('opentestfactory.org/categoryPrefix')
    category = labels.get('opentestfactory.org/category')
    version = labels.get('opentestfactory.org/categoryVersion') or None

    for keys in (
        (prefix, category, version),
        (None, category, version),
        (prefix, category, None),
        (None, category, None),
        (prefix, None, None),
    ):
        if (entry := cache.get(keys)) is not None:
            break
    else:
        return

    declaration, additional_inputs = entry
    for key, definition in declaration.items():
        if key not in inputs:
            if definition.get('required'):
                raise core.ExecutionError(f"Mandatory input '{key}' not provided.")
            if (default := definition.get('default')) is not None:
                inputs[key] = default

    if additional_inputs:
        return

    for key in inputs:
        if key not in declaration and key.replace('_', '-') not in declaration:
            allowed = ', '.join(sorted([f"'{k}'" for k in declaration.keys()]))
            raise core.ExecutionError(
                f"Unexpected input '{key}' found in function step.  Allowed inputs: {allowed}."
            )


def _normalize_inputs(inputs: Dict[str, Any]) -> None:
    """Normalize inputs.

    The 'normalized' form for inputs is with `-` separators, not `_`.

    Non-normalized inputs are removed from the dictionary.

    # Raised exceptions

    A _core.ExecutionError_ is raised if an input is provided twice, in
    a normalized as well as a non-normalized form.
    """
    for key in inputs.copy():
        if '_' in key:
            normalized = key.replace('_', '-')
            if normalized in inputs:
                raise core.ExecutionError(
                    f"Both '{key}' and '{normalized}' specified in inputs."
                )
            inputs[normalized] = inputs.pop(key)


def _dispatch_providercommand(plugin, handler: Handler, body: Dict[str, Any]) -> None:
    """Provider plugin dispatcher.

    `handler` is expected to return either a list of steps or raise a
    _core.ExecutionError_ exception.
    """
    try:
        plugin.logger.debug('Calling provider function %s.', handler.__name__)
        inputs: Dict[str, Any] = body['step'].get('with', {})
        _normalize_inputs(inputs)
        _ensure_inputs_match(plugin, body['metadata'].get('labels', {}), inputs)
        core.publish_providerresult(handler(inputs))
    except core.ExecutionError as err:
        core.publish_error(str(err))
    except Exception as err:
        core.publish_error(f'Unexpected execution error: {err}.')


def _dispatch_executioncommand(_, handler: Handler, body: Dict[str, Any]) -> None:
    """Channel plugin dispatcher."""
    try:
        handler(body)
    except Exception as err:
        core.publish_error(f'Unexpected execution error: {err}.')


def _get_target(
    labels: Dict[str, str], providers: Dict[str, Handler]
) -> Optional[Handler]:
    """Find target for labels.

    Finds the most specific provider.  Returns None if no provider
    matches.

    `prefix/category[@vn]` is more specific than `category[@vn]`.

    `category@vn` is more specific than `category`.

    `category[@vn]` is more specific than `prefix`.
    """
    prefix = labels['opentestfactory.org/categoryPrefix']
    category = labels['opentestfactory.org/category']
    version = labels.get('opentestfactory.org/categoryVersion')

    for template in (f'{prefix}/{category}', category):
        if version:
            parts = version.split('.')
            while parts:
                function = f'{template}@{".".join(parts)}'
                if function in providers:
                    return providers[function]
                parts.pop()
        if template in providers:
            return providers[template]

    return None


def _read_hooks_definition(plugin, hooksfile: str, schema: str) -> None:
    """Read hooks definition file.

    Try to read hooks definition file and set or replace existing hooks
    with those of `hooksfile`.

    # Required parameters

    - plugin: a Flask object
    - hooksfile: a string, the hooks definition file
    - schema: a string, the schema name
    """
    try:
        with open(hooksfile, 'r', encoding='utf-8') as src:
            hooks = yaml.safe_load(src)
        if not isinstance(hooks, dict) or not 'hooks' in hooks:
            plugin.logger.error(
                "Hooks definition file '%s' needs a 'hooks' entry, ignoring.", hooksfile
            )
            return

        config = plugin.config['CONFIG']
        if prev := config.get('hooks'):
            plugin.logger.info("Replacing hooks definition using '%s'.", hooksfile)
        else:
            plugin.logger.info("Reading hooks definition from '%s'.", hooksfile)

        config['hooks'] = hooks['hooks']
        valid, extra = validate_schema(schema, config)
        if valid:
            return

        plugin.logger.error(
            "Error while verifying '%s' hooks definition: %s.", hooksfile, extra
        )
        if prev:
            config['hooks'] = prev
        else:
            try:
                del config['hooks']
            except KeyError:
                pass
    except Exception as err:
        plugin.logger.error(
            "Error while reading '%s' hooks definition: %s.", hooksfile, err
        )


def watch_file(plugin, name: str, schema: str, handler) -> None:
    """Read external definition if env define one."""
    handler(plugin, name, schema)


def _subscribe(
    plugin, cat_prefix: str, cat: str, cat_version: str, manifest: Dict[str, Any]
) -> str:
    """Subscribe for the relevent event."""
    context = plugin.config['CONTEXT']
    kind = context[KIND_KEY]
    labels = {}
    if cat is not None:
        labels['opentestfactory.org/category'] = cat
    if cat_prefix is not None:
        labels['opentestfactory.org/categoryPrefix'] = cat_prefix
    if cat_version is not None:
        labels['opentestfactory.org/categoryVersion'] = cat_version
    context[INPUTS_KEY][(cat_prefix, cat, cat_version)] = (
        manifest.get('inputs', {}),
        manifest.get('additionalInputs'),
    )
    return subscribe(kind=kind, target='inbox', app=plugin, labels=labels)


def run_plugin(plugin):
    """Start and run plugin.

    Subscribe to the relevant events before startup and tries to
    unsbuscribe in case of errors.

    Spurious subscriptions may remain in case of brutal termination.
    """
    try:
        context = plugin.config['CONTEXT']
        context[SUBSCRIPTION_KEY] = []
        context[INPUTS_KEY] = {}
        for manifest in context[MANIFEST_KEY]:
            if 'action' not in manifest.get('metadata', {}):
                continue
            for event in manifest.get('events', []):
                cat_prefix = event.get('categoryPrefix')
                cat = event.get('category')
                if cat or cat_prefix:
                    cat_version = event.get('categoryVersion')
                    context[SUBSCRIPTION_KEY].append(
                        _subscribe(plugin, cat_prefix, cat, cat_version, manifest)
                    )
                else:
                    plugin.logger.warning(
                        "At least one of 'category', 'categoryPrefix' required, ignoring."
                    )

        run_app(plugin)
    finally:
        for subscription_id in plugin.config['CONTEXT'][SUBSCRIPTION_KEY]:
            unsubscribe(subscription_id, app=plugin)


def make_plugin(
    name,
    description: str,
    channel: Optional[Handler] = None,
    generator: Optional[Handler] = None,
    provider: Optional[Handler] = None,
    providers: Optional[Dict[str, Handler]] = None,
    publisher: Optional[Handler] = None,
    manifest=None,
    schema=None,
):
    """Create and return a new plugin service.

    One and only one of `channel`, `generator`, `provider`, `providers`,
    or `publisher` must be specified.

    If no `manifest` is specified, there must be `plugin.yaml` file in
    the same directory as the caller source file.  If none is found the
    execution stops.

    - Create default config
    - Subscribe to eventbus
    - Add publication handler
    - Create service (not started)

    # Required parameters

    - name: a string
    - description: a string
    - `channel`, `generator` or `provider`: a function
    - providers: a dictionary

    # Optional parameters

    - manifest: a dictionary or a list of dictionaries or None
    - schema: a string or None

    # Raised exceptions

    A _ValueError_ exception is raised if the provided parameters are
    invalid.

    # Returned value

    A plugin service (not started).
    """

    def process_inbox():
        try:
            body = request.get_json() or {}
        except Exception as err:
            return make_status_response('BadRequest', f'Could not parse body: {err}.')

        valid, extra = validate_schema(kind, body)
        if not valid:
            return make_status_response(
                'BadRequest', f'Not a valid {kind} request: {extra}.'
            )

        if workflow_id := body.get('metadata', {}).get('workflow_id'):
            g.workflow_id = workflow_id

        if providers:
            labels = body['metadata']['labels']

            if target := _get_target(labels=labels, providers=providers):
                _dispatch_providercommand(plugin, target, body)
            else:
                plugin.logger.warning(f'Labels {labels} not handled by {name}.')
        elif provider:
            _dispatch_providercommand(plugin, provider, body)
        elif channel:
            _dispatch_executioncommand(plugin, channel, body)
        else:
            return make_status_response('BadRequest', 'Not implemented yet.')

        return make_status_response('OK', '')

    if len([_ for _ in (channel, generator, provider, providers, publisher) if _]) != 1:
        raise ValueError(
            "One and only one of 'channel', 'generator', 'provider', 'providers', or 'publisher' is required."
        )
    if (
        manifest is not None
        and not isinstance(manifest, dict)
        and not isinstance(manifest, list)
    ):
        raise ValueError(
            "'manifest', if specified, must be a dictionary or a list of dictionaries."
        )

    kind = (
        EXECUTIONCOMMAND
        if channel
        else GENERATORCOMMAND
        if generator
        else PROVIDERCOMMAND
    )
    if not schema:
        schema = SERVICECONFIG if generator else PROVIDERCONFIG
    configfile = f'conf/{name}.yaml'
    plugin = make_app(name, description, configfile=configfile, schema=schema)
    plugin.route('/inbox', methods=['POST'])(process_inbox)

    if manifest is None:
        manifestfile = 'plugin.yaml'
        try:
            manifestfile = os.path.join(
                os.path.dirname(inspect.stack()[1].filename), manifestfile
            )
            with open(manifestfile, 'r', encoding='utf-8') as definition:
                manifest = list(yaml.safe_load_all(definition))
        except Exception as err:
            plugin.logger.error(
                "Oops, could not get '%s' manifest, aborting: %s.", manifestfile, err
            )
            sys.exit(2)

    if kind == PROVIDERCOMMAND and os.environ.get(f'{name.upper()}_PROVIDER_HOOKS'):
        # plugin.logger.info('Starting hooks definition watch thread.')
        watch_file(
            plugin,
            os.environ[f'{name.upper()}_PROVIDER_HOOKS'],
            schema,
            _read_hooks_definition,
        )

    plugin.config['CONTEXT'][MANIFEST_KEY] = manifest
    plugin.config['CONTEXT'][KIND_KEY] = kind

    core.register_defaultplugin(plugin)

    return plugin
