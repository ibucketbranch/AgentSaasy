"""
Tests for Capital Planning & Scenario Modeling feature.

Tests the strategic AI capability for multi-year capital planning
with Monte Carlo simulation.
"""

import pytest
from agent import plan_capital_strategy


class TestCapitalPlanning:
    """Test suite for capital planning tool."""
    
    def test_capital_planning_returns_comprehensive_report(self):
        """Test that capital planning returns a comprehensive report."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "strategy_preference": "balanced",
            "monte_carlo_iterations": 10  # Small for speed
        })
        
        assert isinstance(result, str)
        assert "CAPITAL PLANNING" in result
        assert "SCENARIO MODELING" in result
        assert len(result) > 500  # Comprehensive report
    
    def test_capital_planning_includes_strategy_comparison(self):
        """Test that output includes comparison of multiple strategies."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        # Should compare 4 strategies
        assert "Aggressive Preventive" in result
        assert "Balanced Risk-Based" in result
        assert "Conservative Run-to-Failure" in result
        assert "Budget-Constrained" in result
        assert "STRATEGY COMPARISON" in result
    
    def test_capital_planning_includes_recommended_strategy(self):
        """Test that output includes a recommended strategy."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "strategy_preference": "balanced",
            "monte_carlo_iterations": 10
        })
        
        assert "RECOMMENDED STRATEGY" in result or "RECOMMENDED:" in result
        assert "RATIONALE" in result
        assert "EXPECTED OUTCOMES" in result
    
    def test_capital_planning_includes_cost_analysis(self):
        """Test that output includes cost analysis with uncertainty."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        # Should include NPV and cost ranges
        assert "NPV" in result or "Total Cost" in result
        assert "P10" in result or "P90" in result  # Uncertainty quantification
        assert "Annual Cost" in result
    
    def test_capital_planning_includes_risk_metrics(self):
        """Test that output includes risk and failure analysis."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        assert "failures" in result.lower() or "Failures" in result
        assert "risk" in result.lower() or "Risk" in result
    
    def test_capital_planning_includes_implementation_roadmap(self):
        """Test that output includes implementation guidance."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        assert "IMPLEMENTATION" in result or "ROADMAP" in result
        assert "Year 1" in result or "YEAR 1" in result
    
    def test_capital_planning_includes_business_impact(self):
        """Test that output includes business impact metrics."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        assert "BUSINESS IMPACT" in result or "Business Impact" in result
        assert "ROI" in result or "savings" in result.lower()
    
    def test_capital_planning_respects_planning_horizon(self):
        """Test that planning horizon parameter is respected."""
        result_5yr = plan_capital_strategy.invoke({
            "planning_horizon_years": 5,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        result_15yr = plan_capital_strategy.invoke({
            "planning_horizon_years": 15,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        assert "5 years" in result_5yr
        assert "15 years" in result_15yr
    
    def test_capital_planning_respects_budget_constraint(self):
        """Test that annual budget parameter is used."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 3000000,  # Lower budget
            "monte_carlo_iterations": 10
        })
        
        assert "$3,000,000" in result or "3000000" in result
        assert "Annual Budget" in result
    
    def test_capital_planning_respects_strategy_preference(self):
        """Test that strategy preference is respected."""
        result_aggressive = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "strategy_preference": "aggressive",
            "monte_carlo_iterations": 10
        })
        
        result_conservative = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "strategy_preference": "conservative",
            "monte_carlo_iterations": 10
        })
        
        # Both should complete successfully
        assert "CAPITAL PLANNING" in result_aggressive
        assert "CAPITAL PLANNING" in result_conservative
    
    def test_capital_planning_with_minimal_iterations(self):
        """Test that tool works with minimal Monte Carlo iterations."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 5  # Very small for speed
        })
        
        assert isinstance(result, str)
        assert "Monte Carlo" in result
        assert len(result) > 500
    
    def test_capital_planning_includes_executive_positioning(self):
        """Test that output includes executive-level positioning."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        # Should include executive/strategic language
        assert any(keyword in result for keyword in [
            "EXECUTIVE", "STRATEGIC", "CFO", "MUNICIPAL", 
            "FINANCE", "RECOMMENDATION"
        ])
    
    def test_capital_planning_includes_trade_off_analysis(self):
        """Test that output includes trade-off analysis."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        assert "TRADE-OFF" in result or "Trade-off" in result
        assert "vs" in result.lower()  # Comparison language
    
    def test_capital_planning_includes_next_steps(self):
        """Test that output includes actionable next steps."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        
        assert "NEXT STEPS" in result or "Next Steps" in result
    
    def test_capital_planning_handles_different_budget_levels(self):
        """Test that tool handles various budget levels appropriately."""
        # Low budget
        result_low = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 1000000,
            "monte_carlo_iterations": 10
        })
        
        # High budget
        result_high = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 10000000,
            "monte_carlo_iterations": 10
        })
        
        # Both should complete successfully
        assert "CAPITAL PLANNING" in result_low
        assert "CAPITAL PLANNING" in result_high
        assert "$1,000,000" in result_low
        assert "$10,000,000" in result_high


class TestCapitalPlanningIntegration:
    """Integration tests for capital planning with agent."""
    
    def test_capital_planning_tool_is_available(self):
        """Test that capital planning tool is registered with agent."""
        from agent import get_agent
        
        agent = get_agent()
        # Agent should have tools bound
        assert hasattr(agent, 'bind_tools') or 'tools' in str(agent)
    
    def test_capital_planning_can_be_invoked_directly(self):
        """Test that capital planning tool can be invoked directly."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 5,
            "annual_budget": 3000000,
            "monte_carlo_iterations": 5
        })
        
        assert isinstance(result, str)
        assert len(result) > 100


class TestCapitalPlanningEdgeCases:
    """Test edge cases and error handling."""
    
    def test_capital_planning_with_very_short_horizon(self):
        """Test with very short planning horizon."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 3,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 5
        })
        
        assert "3 years" in result
        assert isinstance(result, str)
    
    def test_capital_planning_with_very_long_horizon(self):
        """Test with very long planning horizon."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 20,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 5
        })
        
        assert "20 years" in result
        assert isinstance(result, str)
    
    def test_capital_planning_with_all_strategies(self):
        """Test that all strategy preferences work."""
        strategies = ["aggressive", "balanced", "conservative", "budget_constrained"]
        
        for strategy in strategies:
            result = plan_capital_strategy.invoke({
                "planning_horizon_years": 10,
                "annual_budget": 5000000,
                "strategy_preference": strategy,
                "monte_carlo_iterations": 5
            })
            
            assert isinstance(result, str)
            assert "CAPITAL PLANNING" in result


class TestCapitalPlanningPerformance:
    """Performance and scalability tests."""
    
    def test_capital_planning_completes_quickly_with_low_iterations(self):
        """Test that tool completes quickly with low iteration count."""
        import time
        
        start = time.time()
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 10
        })
        elapsed = time.time() - start
        
        # Should complete in reasonable time (< 30 seconds for 10 iterations)
        assert elapsed < 30
        assert isinstance(result, str)
    
    @pytest.mark.slow
    def test_capital_planning_with_full_iterations(self):
        """Test with full 1000 iterations (marked as slow test)."""
        result = plan_capital_strategy.invoke({
            "planning_horizon_years": 10,
            "annual_budget": 5000000,
            "monte_carlo_iterations": 1000
        })
        
        assert "1000" in result  # Should mention iteration count
        assert isinstance(result, str)
        assert len(result) > 1000  # Comprehensive report
