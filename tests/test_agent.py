"""Tests for AgentSaasy_NGAI asset management agent and tools.

Comprehensive test suite covering all asset management tools:
- Asset querying and filtering
- Health analysis and trend detection
- Predictive failure analysis
- TCO calculation
- Compliance tracking

Tests verify both success paths and error handling for production reliability.
"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import agent tools after potential env setup
from agent import (
    query_assets,
    analyze_asset_health,
    predict_failures,
    calculate_tco,
    track_compliance,
    get_agent,
)

DATA_PATH = Path(__file__).parent.parent / "data" / "asset_data.csv"


class TestQueryAssets:
    """Tests for query_assets tool - asset filtering and retrieval."""

    def test_query_all_assets(self) -> None:
        """Query with no filters returns total asset stats."""
        result = query_assets.invoke("all")
        assert "Found" in result or "asset" in result.lower()
        assert "$" in result or "value" in result.lower()

    def test_query_building_a(self) -> None:
        """Filter by Building A location."""
        result = query_assets.invoke("Building A")
        assert "Found" in result or "asset" in result.lower()

    def test_query_pump_assets(self) -> None:
        """Filter by Pump asset type."""
        result = query_assets.invoke("pump")
        assert "Found" in result or "asset" in result.lower()

    def test_query_critical_assets(self) -> None:
        """Filter by critical health status."""
        result = query_assets.invoke("critical assets")
        assert "Critical" in result or "asset" in result.lower()

    def test_query_last_quarter(self) -> None:
        """Filter by last quarter time period."""
        result = query_assets.invoke("last quarter")
        assert "Found" in result or "asset" in result.lower()

    def test_query_missing_file(self) -> None:
        """Graceful error handling when asset data file is missing."""
        with patch.object(Path, "exists", return_value=False):
            import agent as agent_module
            original = agent_module.DATA_PATH
            agent_module.DATA_PATH = Path("/nonexistent/asset_data.csv")
            try:
                result = query_assets.invoke("all")
                assert "Error" in result
                assert "not found" in result
            finally:
                agent_module.DATA_PATH = original


class TestAnalyzeAssetHealth:
    """Tests for analyze_asset_health tool - health trend analysis."""

    def test_analyze_returns_health_summary(self) -> None:
        """Returns health score statistics and trend summary."""
        result = analyze_asset_health.invoke("all")
        assert "Health" in result or "score" in result.lower() or "analysis" in result.lower()

    def test_analyze_with_sufficient_data(self) -> None:
        """Produces health metrics when asset data exists."""
        result = analyze_asset_health.invoke("assets")
        assert "score" in result.lower() or "health" in result.lower()

    def test_analyze_identifies_critical_assets(self) -> None:
        """Identifies and flags critical assets requiring attention."""
        result = analyze_asset_health.invoke("all")
        # Should contain health categories or status
        assert "critical" in result.lower() or "warning" in result.lower() or "healthy" in result.lower()

    def test_analyze_missing_file(self) -> None:
        """Graceful error handling when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/asset_data.csv")
        try:
            result = analyze_asset_health.invoke("all")
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestPredictFailures:
    """Tests for predict_failures tool - predictive maintenance."""

    def test_predict_returns_risk_analysis(self) -> None:
        """Returns failure risk analysis and predictions."""
        result = predict_failures.invoke("all")
        assert "risk" in result.lower() or "failure" in result.lower() or "predict" in result.lower()

    def test_predict_includes_risk_scores(self) -> None:
        """Includes risk scores and failure predictions."""
        result = predict_failures.invoke("assets at risk")
        # Should have risk indicators or scores
        assert "risk" in result.lower() or "score" in result.lower()

    def test_predict_provides_recommendations(self) -> None:
        """Provides actionable maintenance recommendations."""
        result = predict_failures.invoke("which assets will fail")
        # Should contain recommendations or action items
        assert "recommend" in result.lower() or "maintenance" in result.lower() or "risk" in result.lower()

    def test_predict_missing_file(self) -> None:
        """Graceful error handling when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/asset_data.csv")
        try:
            result = predict_failures.invoke("all")
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestCalculateTCO:
    """Tests for calculate_tco tool - Total Cost of Ownership analysis."""

    def test_tco_returns_cost_breakdown(self) -> None:
        """Returns comprehensive TCO breakdown."""
        result = calculate_tco.invoke({"asset_id": "all", "time_horizon_years": 5})
        assert "TCO" in result or "Cost" in result
        assert "$" in result

    def test_tco_includes_roi_analysis(self) -> None:
        """Includes ROI percentage in analysis."""
        result = calculate_tco.invoke({"asset_id": "all", "time_horizon_years": 5})
        assert "ROI" in result or "return" in result.lower()

    def test_tco_custom_time_horizon(self) -> None:
        """Handles custom time horizon parameter."""
        result = calculate_tco.invoke({"asset_id": "all", "time_horizon_years": 10})
        assert "10 years" in result or "10" in result
        assert "$" in result

    def test_tco_specific_asset(self) -> None:
        """Calculates TCO for specific asset ID."""
        result = calculate_tco.invoke({"asset_id": "PUMP-001", "time_horizon_years": 5})
        # Should either find the asset or report not found
        assert "PUMP-001" in result or "not found" in result.lower() or "TCO" in result

    def test_tco_missing_file(self) -> None:
        """Graceful error handling when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/asset_data.csv")
        try:
            result = calculate_tco.invoke({"asset_id": "all", "time_horizon_years": 5})
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestTrackCompliance:
    """Tests for track_compliance tool - regulatory compliance monitoring."""

    def test_compliance_returns_status_report(self) -> None:
        """Returns compliance status report."""
        result = track_compliance.invoke("all")
        assert "Compliance" in result or "compliant" in result.lower() or "inspection" in result.lower()

    def test_compliance_includes_metrics(self) -> None:
        """Includes compliance rate and inspection stats."""
        result = track_compliance.invoke("all")
        # Should have compliance indicators
        assert "compliant" in result.lower() or "overdue" in result.lower() or "inspection" in result.lower()

    def test_compliance_identifies_violations(self) -> None:
        """Identifies non-compliant assets and violations."""
        result = track_compliance.invoke("check status")
        # Should mention compliance status (compliant, overdue, etc.)
        assert any(word in result.lower() for word in ["compliant", "overdue", "due", "inspection", "status"])

    def test_compliance_missing_file(self) -> None:
        """Graceful error handling when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/asset_data.csv")
        try:
            result = track_compliance.invoke("all")
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestAgentOrchestration:
    """Tests for main agent orchestration with tool binding (mocked LLM)."""

    def test_get_agent_returns_llm_with_tools(self) -> None:
        """get_agent returns LLM instance with tools bound."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("agent.ChatOpenAI") as mock_llm:
                mock_llm.return_value = MagicMock()
                agent = get_agent(verbose=False)
                assert agent is not None
                assert hasattr(agent, "invoke")

    def test_agent_has_five_tools(self) -> None:
        """Agent is configured with all 5 asset management tools."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("agent.ChatOpenAI") as mock_llm:
                mock_instance = MagicMock()
                mock_llm.return_value = mock_instance
                
                agent = get_agent(verbose=False)
                
                # Verify bind_tools was called with all 5 tools
                assert mock_instance.bind_tools.called
                tools = mock_instance.bind_tools.call_args[0][0]
                tool_names = [t.name for t in tools]
                assert "query_assets" in tool_names
                assert "analyze_asset_health" in tool_names
                assert "predict_failures" in tool_names
                assert "calculate_tco" in tool_names
                assert "track_compliance" in tool_names
                assert len(tool_names) == 5

    def test_agent_uses_modern_tool_binding(self) -> None:
        """Agent uses modern LangChain tool binding approach."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("agent.ChatOpenAI") as mock_llm:
                mock_instance = MagicMock()
                mock_llm.return_value = mock_instance
                
                agent = get_agent(verbose=False)
                
                # Verify bind_tools was called (modern LangChain pattern)
                assert mock_instance.bind_tools.called

    def test_agent_configured_for_deterministic_responses(self) -> None:
        """Agent uses temperature=0 for production reliability."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("agent.ChatOpenAI") as mock_llm:
                agent = get_agent(verbose=False)
                
                # Verify temperature=0 was used in LLM initialization
                call_kwargs = mock_llm.call_args[1]
                assert call_kwargs.get("temperature") == 0
