"""Pydantic schemas for API request/response validation."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# ─── Switch ───

class SwitchCreate(BaseModel):
    hostname: str = Field(..., min_length=1, max_length=255)
    ip_address: str = Field(..., min_length=7, max_length=45)
    vendor: str = "cisco_ios"
    device_type: str | None = None
    ssh_port: int = 22
    ssh_username: str | None = None
    ssh_password: str | None = None
    location: str | None = None
    tags: str | None = ""
    notes: str | None = None
    # Connection type
    connection_type: str = "ssh"  # "ssh" or "serial"
    # Serial settings
    serial_port: str | None = None
    serial_baud: int = 9600
    serial_databits: int = 8
    serial_parity: str = "N"
    serial_stopbits: int = 1
    serial_timeout: int = 10
    serial_password: str | None = None


class SwitchUpdate(BaseModel):
    hostname: str | None = None
    ip_address: str | None = None
    vendor: str | None = None
    device_type: str | None = None
    ssh_port: int | None = None
    ssh_username: str | None = None
    ssh_password: str | None = None
    location: str | None = None
    tags: str | None = None
    notes: str | None = None
    status: str | None = None
    # Connection type
    connection_type: str | None = None
    serial_port: str | None = None
    serial_baud: int | None = None
    serial_databits: int | None = None
    serial_parity: str | None = None
    serial_stopbits: int | None = None
    serial_timeout: int | None = None
    serial_password: str | None = None


class SwitchOut(BaseModel):
    id: int
    hostname: str
    ip_address: str
    vendor: str
    device_type: str | None = None
    ssh_port: int
    status: str
    os_version: str | None = None
    serial_number: str | None = None
    location: str | None = None
    tags: str | None = ""
    notes: str | None = None
    connection_type: str = "ssh"
    serial_port: str | None = None
    serial_baud: int = 9600
    serial_databits: int = 8
    serial_parity: str = "N"
    serial_stopbits: int = 1
    serial_timeout: int = 10
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


# ─── Config ───

class ConfigBackupOut(BaseModel):
    id: int
    switch_id: int
    config_type: str
    running_config: str
    config_hash: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConfigDiffOut(BaseModel):
    id: int
    switch_id: int
    from_backup_id: int
    to_backup_id: int
    diff_content: str
    summary: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Chat ───

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=128)
    message: str = Field(..., min_length=1)


class ChatMessageOut(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Workflow ───

class WorkflowCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    switch_ids: str | None = None  # comma-separated
    created_by: str | None = None
    ticket_ref: str | None = None


class WorkflowAdvanceRequest(BaseModel):
    approved: bool = False
    result: str | None = None


class WorkflowStepOut(BaseModel):
    id: int
    workflow_id: int
    step_type: str
    status: str
    description: str | None = None
    command: str | None = None
    result: str | None = None
    requires_approval: bool = True
    approved: bool | None = None
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class WorkflowOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str
    switch_ids: str | None = None
    created_by: str | None = None
    approved_by: str | None = None
    ticket_ref: str | None = None
    steps: list[WorkflowStepOut] = []
    created_at: datetime
    updated_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


# ─── Security ───

class SecurityFindingOut(BaseModel):
    id: int
    switch_id: int
    finding_type: str
    severity: str
    title: str
    description: str | None = None
    remediation: str | None = None
    cve_id: str | None = None
    affected_component: str | None = None
    status: str
    created_at: datetime
    resolved_at: datetime | None = None

    model_config = {"from_attributes": True}


class SecurityFindingUpdate(BaseModel):
    status: str = "resolved"  # resolved, false_positive


# ─── Containerlab ───

class ContainerlabTopologyOut(BaseModel):
    id: int
    name: str
    topology_data: Any
    file_path: str | None = None
    node_count: int
    link_count: int
    is_active: bool
    created_at: datetime
    last_synced_at: datetime | None = None

    model_config = {"from_attributes": True}


# ─── Metrics ───

class DeviceMetricOut(BaseModel):
    id: int
    switch_id: int
    cpu_usage: float | None = None
    memory_usage: float | None = None
    temperature: float | None = None
    uptime_seconds: int | None = None
    interface_count: int | None = None
    interfaces_up: int | None = None
    interfaces_down: int | None = None
    recorded_at: datetime

    model_config = {"from_attributes": True}


# ─── Audit ───

class AuditLogOut(BaseModel):
    id: int
    action: str
    actor: str | None = None
    target_type: str | None = None
    target_id: int | None = None
    details: Any | None = None
    status: str
    ip_address: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Dashboard Stats ───

class DashboardStats(BaseModel):
    total_switches: int = 0
    online_switches: int = 0
    offline_switches: int = 0
    total_configs: int = 0
    open_security_findings: int = 0
    active_workflows: int = 0
    total_topologies: int = 0


# ─── Config Templates ───

class ConfigTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    vendor: str = "cisco_ios"
    category: str = "general"
    template_body: str = Field(..., min_length=1)
    variables: Any | None = None
    tags: str | None = ""


class ConfigTemplateUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    vendor: str | None = None
    category: str | None = None
    template_body: str | None = None
    variables: Any | None = None
    tags: str | None = None


class ConfigTemplateOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    vendor: str
    category: str
    template_body: str
    variables: Any | None = None
    tags: str | None = ""
    is_builtin: bool = False
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class TemplateApplyRequest(BaseModel):
    template_id: int
    variables: dict[str, str] = {}
