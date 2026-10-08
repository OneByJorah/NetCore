# NetCore Template System

## Overview

NetCore provides a robust template engine for generating network device configurations from Jinja2 templates. The system supports 50+ built-in templates covering various device vendors (Cisco, Aruba, Juniper, Arista, Linux) and use cases (VLANs, security, routing, interfaces, etc.).

## Template Structure

Templates are organized in the `templates/` directory and follow a consistent naming convention and structure:

```
templates/
├── vendor_name_template_type.j2
├── generic_template_name.j2
├── device_type_specific.j2
└── ... (50+ templates total)
```

### Template Naming Convention

- **Vendor-specific templates**: `{vendor_name}_{description}.j2`
  - `arubaos_full_config.j2`
  - `cisco_ios_access_config.j2`
  - `juniper_junos_routing.j2`

- **Generic templates**: `{use_case}.j2`
  - `vlan_template.j2`
  - `security_config.j2`
  - `routing_config.j2`

- **Device-type templates**: `{device_type}_{feature}.j2`
  - `switch_interface_config.j2`
  - `router_ospf_config.j2`

## Template Categories

### 1. Vendor-Specific Templates

Templates tailored for specific device vendors with vendor-specific syntax and features.

**ArubaOS**:
- `arubaos_full_config.j2` - Complete ArubaOS-Switch/ProCurve configuration

**Cisco IOS**:
- `cisco_ios_access_config.j2` - Access switch configuration
- `cisco_ios_core_config.j2` - Core router configuration
- `cisco_xr_config.j2` - Cisco ASR/XR router configuration

**Juniper JunOS**:
- `juniper_junos_routing.j2` - Routing configuration
- `juniper_junos_security.j2` - Security configuration

**Arista EOS**:
- `arista_eos_interfaces.j2` - Interface configuration
- `arista_eos_routing.j2` - Routing configuration

**Linux**:
- `linux_switch_config.j2` - Linux-based switch configuration

### 2. Generic Templates

Device-agnostic templates that work across multiple vendors.

- `vlan_template.j2` - VLAN configuration template
- `security_template.j2` - Security policies template
- `routing_template.j2` - Routing configuration template
- `interface_template.j2` - Interface configuration template

### 3. Device-Type Templates

Templates specific to device types (switch vs router).

- `switch_access_config.j2` - Access switch configuration
- `switch_core_config.j2` - Core switch configuration
- `router_access_config.j2` - Access router configuration

## Template Variables

Each template can use various variables to customize the generated configuration:

### Network Variables
- `hostname` - Device hostname
- `default_gateway` - Default gateway IP
- `timezone` - Timezone setting
- `ospf_area` - OSPF area ID

### VLAN Variables
- `vlans` - List of VLAN objects with attributes:
  - `id` - VLAN ID
  - `name` - VLAN name
  - `untagged` - Untagged ports
  - `tagged` - Tagged ports
  - `ip` - VLAN IP address
  - `mask` - VLAN subnet mask
  - `helper` - DHCP helper address

### Security Variables
- `radius_servers` - List of RADIUS servers
  - `host` - Server IP
  - `key` - Authentication key
- `snmpv3` - Enable SNMPv3 security
- `snmp_contact` - Contact information
- `snmp_server_community` - SNMP community strings

### Interface Variables
- `access_ports` - Access port list
- `sflow_ports` - sFlow sampling ports
- `trust_ports` - Trusted ports for DHCP
- `backbone_vlan` - Backbone VLAN ID
- `backbone_port` - Backbone port interface

### Features and Protocols
- `role` - Device role (`switch` or `router`)
- `ip_routing` - Enable IP routing
- `router_ospf` - Enable OSPF
- `snmpv3_enable` - Enable SNMPv3
- `dhcp_option82` - Enable DHCP Option 82
- `loop_protect` - Loop protection settings
- `spanning_tree` - Spanning tree configuration

## Template Usage

### Rendering a Template

Use the NetCore CLI or API to render a template:

```bash
# Using CLI
cd scripts
python cli.py render --hostname SW01 --mgmt-ip 192.168.1.10 --role access

# Or use API endpoint
POST /api/templates/render
{
  "template_name": "arubaos_full_config.j2",
  "variables": {
    "hostname": "SW01",
    "role": "access",
    "default_gateway": "192.168.1.1",
    "timezone": -240
  }
}
```

### Template Variables Reference

#### Required Variables
- `hostname` - Device hostname

#### Optional Variables
- `role` - Device role (`switch` or `router`)
- `default_gateway` - Default gateway IP
- `timezone` - Timezone offset in hours
- `ospf_area` - OSPF area ID
- `vlan_list` - List of VLAN configurations
- `radius_servers` - List of RADIUS servers
- `snmpv3` - Enable SNMPv3
- `snmp_contact` - Contact information
- `access_ports` - Access port list
- `sflow_ports` - sFlow sampling ports
- `trust_ports` - Trusted ports
- `backbone_vlan` - Backbone VLAN ID
- `backbone_port` - Backbone port interface

### Template Rendering Process

1. **Template Selection**: Choose the appropriate template based on vendor and use case
2. **Variable Preparation**: Prepare the template variables
3. **Template Rendering**: Use Jinja2 to render the template
4. **Configuration Validation**: Validate the generated configuration
5. **Deployment**: Deploy the configuration to the device

## Template Development

### Creating New Templates

To create a new template:

1. **Create the template file** in `templates/` directory
2. **Define the Jinja2 syntax** with proper ArubaOS/ProCurve configuration commands
3. **Document variables** used in the template
4. **Test the template** with sample variables

### Template Best Practices

1. **Consistent naming**: Follow the established naming convention
2. **Modular design**: Use inheritance for common template sections
3. **Comprehensive variable documentation**: Document all template variables
4. **Validation**: Validate template output before deployment
5. **Testing**: Test templates with various input scenarios

## Built-in Templates

### Current Available Templates

**ArubaOS/ProCurve**:
- `arubaos_full_config.j2` - Complete ArubaOS-Switch configuration

**Cisco IOS**:
- `cisco_ios_access_config.j2` - Access switch configuration
- `cisco_ios_core_config.j2` - Core router configuration

**Juniper JunOS**:
- `juniper_junos_routing.j2` - Routing configuration
- `juniper_junos_security.j2` - Security configuration

**Arista EOS**:
- `arista_eos_interfaces.j2` - Interface configuration

**Linux**:
- `linux_switch_config.j2` - Linux-based switch configuration

### Template Examples

#### ArubaOS Full Config Template

```jinja2
{#- ArubaOS-Switch / ProCurve standard config generator -#}
hostname "{{ hostname }}"
time timezone {{ timezone | default(-240) }}

{% if role == "access" and default_gateway %}
ip default-gateway {{ default_gateway }}
{% endif %}

timesync sntp

{% if snmpv3 %}
snmpv3 enable
snmpv3 only
snmpv3 restricted-access
snmpv3 user "swmonitor"
snmpv3 group OperatorAuth user "swmonitor" sec-model ver3
{% endif %}

snmp-server community "public" operator unrestricted
snmp-server community "netadmin" operator unrestricted

{% if radius_servers %}
aaa authentication login privilege-mode
aaa authentication console login radius local
aaa authentication console enable radius local
aaa authentication telnet login radius local
aaa authentication telnet enable radius local
aaa authentication web login radius local
aaa authentication ssh login radius local
aaa authentication ssh enable radius local

{% for r in radius_servers %}
radius-server host {{ r.host }} key "{{ r.key }}"
{% endfor %}
{% endif %}
```

## Template Integration

### API Integration

The NetCore API provides endpoints for template operations:

- `GET /api/templates/` - List all available templates
- `POST /api/templates/render` - Render a template with variables
- `POST /api/config/render` - Render configuration and deploy to device

### CLI Integration

The NetCore CLI provides template rendering capabilities:

```bash
# List available templates
NetCore templates list

# Render a template
cd scripts
python cli.py render --template arubaos_full_config.j2 --hostname SW01 --role access
```

## Template Validation

### Configuration Validation

Generated configurations are validated for:
- Syntax correctness
- Required parameter presence
- Device compatibility
- Security compliance

### Template Testing

Templates are tested with various scenarios:
- Edge cases (empty values, special characters)
- Different device types
- Various vendor-specific syntax
- Large configuration sizes

## Future Enhancements

### Planned Template Additions

1. **Cisco Nexus templates**: NX-OS configuration templates
2. **Huawei templates**: Huawei VRRP and stacking configurations
3. **Template inheritance**: Support for template inheritance and mixins
4. **Template versioning**: Template versioning and rollback support
5. **Template marketplace**: Community template marketplace
6. **Template automation**: Automated template generation based on device profiles

## Documentation

This documentation is continuously updated as new templates are added and the template system evolves. For the most up-to-date information, refer to the NetCore GitHub repository.

---

*Last updated: Current release*
*Template version: 1.0*