"""Tests for the AgentSaasy agent and tools."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import after potential env setup
from agent import (
    query_data,
    analyze_trends,
    detect_anomalies,
    generate_forecast,
    summarize_insights,
    get_agent,
)

DATA_PATH = Path(__file__).parent.parent / "data" / "sales_data.csv"


class TestQueryData:
    """Tests for query_data tool."""

    def test_query_all_data(self) -> None:
        """Query with no filters returns total stats."""
        result = query_data.invoke("all")
        assert "Found" in result
        assert "Total amount" in result
        assert "$" in result

    def test_query_north_region(self) -> None:
        """Filter by North region."""
        result = query_data.invoke("North region")
        assert "Found" in result
        assert "Total amount" in result

    def test_query_widget_a(self) -> None:
        """Filter by Widget A product."""
        result = query_data.invoke("Widget A")
        assert "Found" in result

    def test_query_last_quarter(self) -> None:
        """Filter by last quarter."""
        result = query_data.invoke("last quarter")
        assert "Found" in result

    def test_query_missing_file(self) -> None:
        """Graceful error when data file is missing."""
        with patch.object(Path, "exists", return_value=False):
            # Need to patch at module level - data path is in agent module
            import agent as agent_module
            original = agent_module.DATA_PATH
            agent_module.DATA_PATH = Path("/nonexistent/sales_data.csv")
            try:
                result = query_data.invoke("all")
                assert "Error" in result
                assert "not found" in result
            finally:
                agent_module.DATA_PATH = original


class TestAnalyzeTrends:
    """Tests for analyze_trends tool."""

    def test_analyze_returns_summary(self) -> None:
        """Returns growth and trend summary."""
        result = analyze_trends.invoke("all")
        assert "Trends" in result or "Growth" in result or "monthly" in result

    def test_analyze_with_sufficient_data(self) -> None:
        """Produces numeric metrics when data exists."""
        result = analyze_trends.invoke("sales")
        assert "$" in result
        assert "%" in result or "monthly" in result

    def test_analyze_missing_file(self) -> None:
        """Graceful error when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/sales_data.csv")
        try:
            result = analyze_trends.invoke("all")
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestDetectAnomalies:
    """Tests for detect_anomalies tool."""

    def test_detect_returns_result(self) -> None:
        """Returns anomaly detection result."""
        result = detect_anomalies.invoke("all")
        assert "Mean" in result or "anomaly" in result.lower() or "No anomalies" in result

    def test_detect_includes_stats(self) -> None:
        """Includes statistical measures."""
        result = detect_anomalies.invoke("full dataset")
        assert "$" in result

    def test_detect_missing_file(self) -> None:
        """Graceful error when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/sales_data.csv")
        try:
            result = detect_anomalies.invoke("all")
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestGenerateForecast:
    """Tests for generate_forecast tool."""

    def test_forecast_returns_predictions(self) -> None:
        """Returns forecast with predictions."""
        result = generate_forecast.invoke({"periods": 4})
        assert "Forecast" in result or "Week" in result
        assert "R²" in result or "R-squared" in result.lower()

    def test_forecast_includes_metrics(self) -> None:
        """Includes R² score and dollar amounts."""
        result = generate_forecast.invoke({"periods": 2})
        assert "$" in result
        assert "Week" in result

    def test_forecast_custom_periods(self) -> None:
        """Handles custom period parameter."""
        result = generate_forecast.invoke({"periods": 8})
        assert "Week 8" in result or "week 8" in result.lower()

    def test_forecast_missing_file(self) -> None:
        """Graceful error when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/sales_data.csv")
        try:
            result = generate_forecast.invoke({"periods": 4})
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestSummarizeInsights:
    """Tests for summarize_insights tool."""

    def test_summary_returns_executive_summary(self) -> None:
        """Returns executive summary format."""
        result = summarize_insights.invoke({"context": ""})
        assert "EXECUTIVE SUMMARY" in result or "Total Revenue" in result

    def test_summary_includes_key_metrics(self) -> None:
        """Includes revenue, product, and region metrics."""
        result = summarize_insights.invoke({"context": ""})
        assert "$" in result
        assert "Product" in result or "Region" in result

    def test_summary_with_context(self) -> None:
        """Includes provided context in summary."""
        result = summarize_insights.invoke({"context": "Q4 analysis"})
        assert "Q4 analysis" in result or "Context" in result

    def test_summary_missing_file(self) -> None:
        """Graceful error when data file is missing."""
        import agent as agent_module
        original = agent_module.DATA_PATH
        agent_module.DATA_PATH = Path("/nonexistent/sales_data.csv")
        try:
            result = summarize_insights.invoke({"context": ""})
            assert "Error" in result
        finally:
            agent_module.DATA_PATH = original


class TestAgentBehavior:
    """Tests for main agent orchestration (mocked LLM)."""

    def test_get_agent_returns_executor(self) -> None:
        """get_agent returns an AgentExecutor."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("agent.ChatOpenAI") as mock_llm:
                mock_llm.return_value = MagicMock()
                agent = get_agent(verbose=False)
                assert agent is not None
                assert hasattr(agent, "invoke")

    def test_agent_has_three_tools(self) -> None:
        """Agent is configured with all 5 tools."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("agent.ChatOpenAI") as mock_llm:
                # Mock the LLM and bind_tools method
                mock_instance = MagicMock()
                mock_llm.return_value = mock_instance
                
                agent = get_agent(verbose=False)
                
                # Verify bind_tools was called with all 5 tools
                assert mock_instance.bind_tools.called
                tools = mock_instance.bind_tools.call_args[0][0]
                tool_names = [t.name for t in tools]
                assert "query_data" in tool_names
                assert "analyze_trends" in tool_names
                assert "detect_anomalies" in tool_names
                assert "generate_forecast" in tool_names
                assert "summarize_insights" in tool_names
                assert len(tool_names) == 5

    def test_agent_uses_tool_binding(self) -> None:
        """Agent uses modern tool binding approach."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("agent.ChatOpenAI") as mock_llm:
                mock_instance = MagicMock()
                mock_llm.return_value = mock_instance
                
                agent = get_agent(verbose=False)
                
                # Verify bind_tools was called (modern approach)
                assert mock_instance.bind_tools.called
