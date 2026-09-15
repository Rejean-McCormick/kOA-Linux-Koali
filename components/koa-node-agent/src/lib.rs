#![forbid(unsafe_code)]

//! kOA Node Agent bounded library surface.
//!
//! The crate also contains private broker, transport, and fixed host-adapter
//! layers used by dedicated binaries. This library root intentionally exposes
//! only bounded domain/application/configuration/health/receipt APIs and never
//! a generic shell or arbitrary privileged-operation interface.

pub mod application;
pub mod config;
pub mod domain;
pub mod health;
pub mod receipts;

use config::{
    ConfigurationError, NodeAgentConfig, OperationClass, COMPONENT_ID, COMPONENT_VERSION,
};
use health::{evaluate_health, HealthSnapshot, RuntimeEvidence};
use std::error::Error;
use std::fmt;
use std::path::Path;

pub const DISPLAY_NAME: &str = "kOA Node Agent";
pub const INTERFACE_VERSION: &str = "1.0.0";
pub const PUBLIC_COMMANDS: [&str; 3] = [
    "execute_node_operation",
    "cancel_node_operation",
    "acknowledge_recovery_result",
];
pub const PUBLIC_QUERIES: [&str; 3] = [
    "get_node_agent_capabilities",
    "get_node_operation_status",
    "get_node_agent_health",
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BootstrapError {
    message: String,
}

impl BootstrapError {
    fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

impl fmt::Display for BootstrapError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.message)
    }
}

impl Error for BootstrapError {}

impl From<ConfigurationError> for BootstrapError {
    fn from(error: ConfigurationError) -> Self {
        Self::new(error.to_string())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NodeAgentRuntime {
    config: NodeAgentConfig,
    evidence: RuntimeEvidence,
    status: HealthSnapshot,
}

impl NodeAgentRuntime {
    pub fn config(&self) -> &NodeAgentConfig {
        &self.config
    }

    pub fn evidence(&self) -> &RuntimeEvidence {
        &self.evidence
    }

    pub fn status(&self) -> &HealthSnapshot {
        &self.status
    }

    pub fn enabled_operation_classes(&self) -> Vec<OperationClass> {
        self.config
            .enabled_operation_classes
            .iter()
            .copied()
            .collect()
    }

    pub fn refresh_evidence(&mut self, evidence: RuntimeEvidence) {
        self.status = evaluate_health(&self.config, &evidence);
        self.evidence = evidence;
    }
}

pub fn bootstrap(
    config_path: Option<&Path>,
    evidence: RuntimeEvidence,
) -> Result<NodeAgentRuntime, BootstrapError> {
    let config = NodeAgentConfig::load(config_path)?;
    bootstrap_with_config(config, evidence)
}

pub fn bootstrap_with_config(
    config: NodeAgentConfig,
    evidence: RuntimeEvidence,
) -> Result<NodeAgentRuntime, BootstrapError> {
    config.validate()?;
    if evidence.active_request_id.is_some() != evidence.active_operation_class.is_some() {
        return Err(BootstrapError::new(
            "active request identity and operation class must be reported together",
        ));
    }
    let status = evaluate_health(&config, &evidence);
    Ok(NodeAgentRuntime {
        config,
        evidence,
        status,
    })
}

pub fn describe_json() -> String {
    let commands = PUBLIC_COMMANDS
        .iter()
        .map(|value| format!("\"{value}\""))
        .collect::<Vec<_>>()
        .join(",");
    let queries = PUBLIC_QUERIES
        .iter()
        .map(|value| format!("\"{value}\""))
        .collect::<Vec<_>>()
        .join(",");
    format!(
        concat!(
            "{{\"component_id\":\"{}\",",
            "\"display_name\":\"{}\",",
            "\"version\":\"{}\",",
            "\"interface_version\":\"{}\",",
            "\"public_commands\":[{}],",
            "\"public_queries\":[{}],",
            "\"arbitrary_privileged_interface\":false,",
            "\"partial_authoritative_activation\":false}}"
        ),
        COMPONENT_ID, DISPLAY_NAME, COMPONENT_VERSION, INTERFACE_VERSION, commands, queries
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bootstrap_does_not_create_paths_or_enable_operations() {
        let config = NodeAgentConfig::default();
        let runtime = bootstrap_with_config(config, RuntimeEvidence::default())
            .expect("default bootstrap is structurally valid");
        assert!(runtime.enabled_operation_classes().is_empty());
        assert_eq!(runtime.status().readiness, "not_ready");
    }

    #[test]
    fn active_request_evidence_is_consistent() {
        let evidence = RuntimeEvidence {
            active_request_id: Some("request-1".to_owned()),
            ..RuntimeEvidence::default()
        };
        assert!(bootstrap_with_config(NodeAgentConfig::default(), evidence).is_err());
    }

    #[test]
    fn description_has_only_registered_public_interfaces() {
        let description = describe_json();
        assert!(description.contains("execute_node_operation"));
        assert!(description.contains("get_node_agent_health"));
        assert!(!description.contains("shell"));
    }
}
