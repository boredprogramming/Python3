"""
These are custom table views to use in conjunction with PyEZ to filter out the information i needed
for daily reports.

These are currently based on RPC calls.
if you need to see which rpc call is used for each command, postend a command with a "| display xml rpc"

"""

"""
BEGINNING OF YML VARIABLES
"""

ShowChassisAlarms = """
---
ShowChassisAlarms: 
    command: show system alarms
    key: Class
    view: _chassis_alarm_view
    
_chassis_alarm_view: 
    columns: 
        alarm_time: Alarm time
        alarm_class: Class
        alarm_description: Description
"""



ShowSoftwareVersion = """
---
ShowSoftwareVersion:
    rpc: get-software-information
    item: .//re-name[starts-with(.,'fpc')]/parent::*
    view: _software_version_view

_software_version_view:
    fields:
        name: .//software-information/package-information/name
        comment: .//software-information/package-information/comment
"""

ShowVirtualChassis = """
---
ShowVirtualChassis:
    rpc: get-virtual-chassis-information
    item: //virtual-chassis-information/member-list/member
    view: _virtual_chassis_view

_virtual_chassis_view:
    fields:
        member_id: member-id
        member_status: member-status
        fpc_slot: fpc-slot
        member_serial_number: member-serial-number
        member_model: member-model
        member_priority: member-priority
        member_role: member-role
"""

ShowSoftwareVersionFPC0 = """
---
ShowSoftwareVersionFPC0:
    rpc: get-software-information
    item: //multi-routing-engine-item[1]/software-information/package-information
    view: _software_version_fpc_0_view

_software_version_fpc_0_view:
    fields:
        name: name
        comment: comment
"""


ShowSoftwareVersionFPC1 = """
---
ShowSoftwareVersionFPC1:
    rpc: get-software-information
    item: //multi-routing-engine-item[2]/software-information/package-information
    view: _software_version_fpc_1_view

_software_version_fpc_1_view:
    fields:
        name: name
        comment: comment
"""

"""
PEM - Break out to only pull FPC 0 or FPC 1 as only two are in 
a stack currently in a normal deployment
"""

ChassisEnvironmentPEM = """
---
ChassisEnvironmentPEM:
    rpc: get-environment-pem-information
    item: .//name[starts-with(.,'FPC')]/parent::*
    key: environment-component-item
    view: _environment_pem_view
    args:
        member: '{}'
        
_environment_pem_view:
    fields:
        name: name
        state: state
"""


FpcHwTable = """
---

# -------------------------------------------------------------------
# Table
# -------------------------------------------------------------------
# retrieve the chassis hardware (inventory) and extract the FPC
# items.
# -------------------------------------------------------------------

FpcHwTable:
    rpc: get-chassis-inventory
    item: .//name[starts-with(.,'FPC')]/parent::*
    view: _fpc_hw_view

FpcMiReHwTable:
    rpc: get-chassis-inventory
    item: .//name[starts-with(.,'FPC')]/parent::*
    key:
        - ancestor::multi-routing-engine-item/re-name
        - name
    view: _fpc_hw_view

# -------------------------------------------------------------------
# View
# -------------------------------------------------------------------
# use the underscore (_) so this definition is not
# imported into the glboal namespace. We want to extract various
# bits of information from the FPC items
# -------------------------------------------------------------------

_fpc_hw_view:
    fields:
        name: name
        sn: serial-number
        pn: part-number
        desc: description
        ver: version
        model: model-number    
"""

FPCChassisSubModules = """
---
FPCChassisSubModules:
    rpc: get-chassis-inventory
    item: .//name[starts-with(.,'PIC') or starts-with(.,'Power') or starts-with(.,'Fan')]/parent::*
    key: chassis-sub-module
    view: _chassis_sub_modules_view

_chassis_sub_modules_view:
    fields:
        name: name
        pn: part-number
        sn: serial-number
        description: description
        clei_code: clei-code
        model_number: model-number
"""

FPCChassisSubModulesPICInformation = """
---
FPCChassisSubModulesPICInformation:
    rpc: get-chassis-inventory
    item: .//name[starts-with(.,'FPC')]/parent::*
    key: chassis-module/name
    view: _chassis_module_view

_chassis_module_view:
    fields:
        fpc: name
        pic: .//chassis-sub-module/name[starts-with(.,'PIC')]
        xcvr: .//chassis-sub-sub-module/name[starts-with(.,'Xcvr')]
        xcvr_version: .//chassis-sub-sub-module/version
        xcvr_part_number: .//chassis-sub-sub-module/part-number
        xcvr_serial_number: .//chassis-sub-sub-module/serial-number
        xcvr_description: .//chassis-sub-sub-module/description
        
"""

FPCChassisSubModulesPICInformationDetail = """
---
FPCChassisSubModulesPICInformationDetail:
    rpc: get-pic-detail
    item: .//pic-detail/parent::*
    key: pic-detail/port-information/port/port-number
    args:
        fpc-slot: '{}'
        pic-slot: '{}'
    view: _pic_detail_view

_pic_detail_view:
    fields:
        slot: .//pic-detail/slot
        pic_slot: .//pic-detail/pic-slot
        port_number: .//pic-detail/port-information/port/port-number
        cable_type: .//pic-detail/port-information/port/cable-type
        fiber_mode: .//pic-detail/port-information/port/fiber-mode
        wavelength: .//pic-detail/port-information/port/wavelength
        
"""

interfaceDiagnosticsOptics = """
---
interfaceDiagnosticsOptics:
    rpc: get-interface-optics-diagnostics-information
    item: .//physical-interface/optics-diagnostics/parent::*
    key: .//physical-interface/name
    view: _interface_diagnostics_view

_interface_diagnostics_view:
    fields:
        name: name[starts-with(.,'xe') or starts-with(.,'ge') or starts-with(.,'et')]
        laser_output_power_dbm: .//optics-diagnostics/laser-output-power-dbm
        rx_signal_avg_optical_power_dbm: .//optics-diagnostics/rx-signal-avg-optical-power-dbm
        laser_bias_current_high_alarm: .//optics-diagnostics/laser-bias-current-high-alarm
        laser_bias_current_low_alarm: .//optics-diagnostics/laser-bias-current-low-alarm
        laser_bias_current_high_warn: .//optics-diagnostics/laser-bias-current-high-warn
        laser_bias_current_low_warn: .//optics-diagnostics/laser-bias-current-low-warn
        laser_tx_power_high_alarm: .//optics-diagnostics/laser-tx-power-high-alarm
        laser_tx_power_low_alarm: .//optics-diagnostics/laser-tx-power-low-alarm
        laser_tx_power_high_warn: .//optics-diagnostics/laser-tx-power-high-warn
        laser_tx_power_low_warn: .//optics-diagnostics/laser-tx-power-low-warn
        module_temperature_high_alarm: .//optics-diagnostics/module-temperature-high-alarm
        module_temperature_high_warn: .//optics-diagnostics/module-temperature-high-warn
        module_temperature_low_warn: .//optics-diagnostics/module-temperature-low-warn
        module_voltage_high_alarm: .//optics-diagnostics/module-voltage-high-alarm
        module_voltage_low_alarm: .//optics-diagnostics/module-voltage-low-alarm
        module_voltage_high_warn: .//optics-diagnostics/module-voltage-high-warn
        module_voltage_low_warn: .//optics-diagnostics/module-voltage-low-warn
        laser_rx_power_high_alarm: .//optics-diagnostics/laser-rx-power-high-alarm
        laser_rx_power_low_alarm: .//optics-diagnostics/laser-rx-power-low-alarm
        laser_rx_power_high_warn: .//optics-diagnostics/laser-rx-power-high-warn
        laser_rx_power_low_warn: .//optics-diagnostics/laser-rx-power-low-warn
        lane_index: .//optics-diagnostics/optics-diagnostics-lane-values/lane-index
        laser_output_power_dbm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-output-power-dbm
        laser_rx_optical_power_dbm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-optical-power-dbm
        laser_bias_current_high_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-high-alarm
        laser_bias_current_low_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-low-alarm
        laser_bias_current_high_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-high-warn
        laser_bias_current_low_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-low-warn
        laser_rx_power_high_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-high-alarm
        laser_rx_power_low_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-low-alarm
        laser_rx_power_high_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-high-warn
        laser_rx_power_low_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-low-warn
        tx_loss_of_signal_functionality_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/tx-loss-of-signal-functionality-alarm
        rx_loss_of_signal_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/rx-loss-of-signal-alarm
        tx_laser_disabled_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/tx-laser-disabled-alarm

"""


"""
END OF YML VARIABLES
"""
