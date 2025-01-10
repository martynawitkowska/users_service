

import re


def add_x_tenant_id_header(result, generator, request, public, **kwargs):
	"""
	Add `X-Tenant-ID` header to all API operations except specific excluded endpoints (e.g., token-related endpoints).
	"""

	if 'components' not in result:
		result['components'] = {}
	if 'parameters' not in result['components']:
		result['components']['parameters'] = {}

	result['components']['parameters']['X-Tenant-ID'] = {
		'name': 'X-Tenant-ID',
		'in': 'header',
		'description': 'Tenant ID required for all requests.',
		'required': True,
		'schema': {'type': 'string'},
	}

	excluded_paths = [
		r'^/token/refresh/',
		r'^/token/',
	]

	excluded_patterns = [re.compile(pattern) for pattern in excluded_paths]

	for path, methods in result.get('paths', {}).items():
		exclude_path = any(pattern.match(path) for pattern in excluded_patterns)

		for operation, operation_schema in methods.items():
			if exclude_path:
				continue

			if 'parameters' not in operation_schema:
				operation_schema['parameters'] = []

			if not any(
				param.get('$ref') == '#/components/parameters/X-Tenant-ID' for param in operation_schema['parameters']
			):
				operation_schema['parameters'].append({'$ref': '#/components/parameters/X-Tenant-ID'})

	return result
