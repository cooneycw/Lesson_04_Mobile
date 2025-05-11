import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec


def demonstrate_risk_pooling(accident_probability=0.05, num_policyholders=100, seed=42, return_fig=False,
                             is_mobile=False):
    """
    Demonstrates the concept of risk pooling in insurance

    Parameters:
    -----------
    accident_probability : float
        The probability of an accident
    num_policyholders : int
        The number of policyholders
    seed : int
        Random seed for reproducibility
    return_fig : bool
        If True, returns the figure and stats for Shiny integration
    is_mobile : bool
        Whether to use mobile-optimized visualization

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object (if return_fig is True)
    stats : dict
        Key statistics (if return_fig is True)
    """
    # Mobile optimizations for plot readability
    if is_mobile:
        # Increase font sizes for mobile scrollable view
        plt.rcParams.update({
            'font.size': 16,  # Larger base font size
            'axes.titlesize': 18,  # Larger title font
            'axes.labelsize': 16,  # Larger axis labels
            'xtick.labelsize': 14,  # Larger x tick labels
            'ytick.labelsize': 14,  # Larger y tick labels
            'legend.fontsize': 14,  # Larger legend text
            'figure.titlesize': 20  # Larger figure title
        })

        # Use brighter, more distinct colors for mobile
        plt.rcParams.update({
            'axes.prop_cycle': plt.cycler(
                color=['#3498DB', '#2ECC71', '#E74C3C', '#9B59B6', '#F39C12', '#1ABC9C']),
        })

    # Fixed claim amount at $20,000
    CLAIM_AMOUNT = 20000

    # Set random seed for consistent results
    np.random.seed(seed)

    # Run the simulation - generate random accidents
    accidents = np.random.random(num_policyholders) < accident_probability

    # Calculate results
    individual_costs = np.where(accidents, CLAIM_AMOUNT, 0)
    total_losses = np.sum(individual_costs)
    fair_premium = accident_probability * CLAIM_AMOUNT
    pool_premium_total = fair_premium * num_policyholders

    # Calculate stats
    num_with_loss = np.sum(accidents)
    percent_with_loss = np.mean(accidents) * 100
    pool_performance = total_losses / pool_premium_total

    # For Shiny integration
    if return_fig:
        if is_mobile:
            # MOBILE OPTIMIZATIONS:
            # Use much larger figure size to prevent flattening
            fig = Figure(figsize=(7, 20))  # Extremely tall figure for mobile

            # Use GridSpec for better control over subplot layout
            gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.6)
            ax1 = fig.add_subplot(gs[0])  # Individual outcomes
            ax2 = fig.add_subplot(gs[1])  # Pool outcomes

            # Make everything bolder and larger for mobile
            linewidth = 3
            fontsize_title = 18
            fontsize_labels = 16
            fontsize_annotations = 14

            # PLOT 1: Simplified visualization for mobile
            # Just show two bars - potential loss vs premium
            bars1 = ax1.bar(
                ['Risk', 'Insurance'],
                [CLAIM_AMOUNT, fair_premium],
                color=['#FF9999', '#99CC99'],
                alpha=0.9,
                width=0.6,
                linewidth=linewidth,
                edgecolor=['#CC6666', '#66CC66']
            )

            # Add bold bar labels - make them stand out more
            ax1.text(0, CLAIM_AMOUNT / 2, f"${CLAIM_AMOUNT:,}",
                     ha='center', va='center', fontsize=fontsize_annotations + 2,
                     fontweight='bold', color='#990000')

            ax1.text(1, fair_premium / 2, f"${fair_premium:,.0f}",
                     ha='center', va='center', fontsize=fontsize_annotations + 2,
                     fontweight='bold', color='#006600')

            # Add clear annotations above bars with better contrasting backgrounds
            ax1.annotate(
                f"{percent_with_loss:.1f}% face\nthis loss",
                xy=(0, CLAIM_AMOUNT),
                xytext=(0, CLAIM_AMOUNT * 1.05),
                ha='center', fontsize=fontsize_annotations,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFEEEE", alpha=0.9, edgecolor='#CC6666')
            )

            ax1.annotate(
                "Everyone\npays this",
                xy=(1, fair_premium),
                xytext=(1, fair_premium * 1.3),
                ha='center', fontsize=fontsize_annotations,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#EEFFEE", alpha=0.9, edgecolor='#66CC66')
            )

            # Clean up plot with bolder elements
            ax1.set_ylabel('Amount ($)', fontsize=fontsize_labels, fontweight='bold')
            ax1.set_title('Individual Risk vs. Insurance', fontsize=fontsize_title, fontweight='bold')
            ax1.grid(axis='y', alpha=0.4, linestyle='--', linewidth=1.5)
            ax1.set_ylim(0, CLAIM_AMOUNT * 1.2)
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

            # Make axis lines thicker for better visibility
            ax1.spines['bottom'].set_linewidth(linewidth)
            ax1.spines['left'].set_linewidth(linewidth)
            ax1.tick_params(width=linewidth - 1, length=10)

            # PLOT 2: Simplified pool visualization with better colors
            outcome_is_surplus = pool_performance < 1

            # Choose colors based on outcome - blue for surplus, red for deficit
            if outcome_is_surplus:
                bar_colors = ['#99CC99', '#9999FF']  # Green premium, blue claims
                bar_edges = ['#66CC66', '#6666FF']
            else:
                bar_colors = ['#99CC99', '#FF9999']  # Green premium, red claims
                bar_edges = ['#66CC66', '#FF6666']

            # Create bars with thicker edges
            bars2 = ax2.bar(
                ['Premiums', 'Claims'],
                [pool_premium_total, total_losses],
                color=bar_colors, alpha=0.9, width=0.6,
                linewidth=linewidth, edgecolor=bar_edges
            )

            # Add bold value labels on bars - larger and more prominent
            ax2.text(0, pool_premium_total / 2, f"${pool_premium_total:,.0f}",
                     ha='center', va='center', fontsize=fontsize_annotations + 2,
                     fontweight='bold', color='#006600')

            claim_color = '#000099' if outcome_is_surplus else '#990000'
            ax2.text(1, total_losses / 2, f"${total_losses:,.0f}",
                     ha='center', va='center', fontsize=fontsize_annotations + 2,
                     fontweight='bold', color=claim_color)

            # Add clear outcome box - more prominent with better styling
            outcome_word = "SURPLUS" if outcome_is_surplus else "DEFICIT"
            outcome_color = "#EEFFEE" if outcome_is_surplus else "#FFEEEE"
            text_color = "#006600" if outcome_is_surplus else "#990000"
            edge_color = "#66CC66" if outcome_is_surplus else "#FF6666"

            ax2.text(0.5, 0.95,
                     f"{outcome_word}: ${abs(pool_premium_total - total_losses):,.0f}",
                     transform=ax2.transAxes, ha='center', va='top', fontsize=fontsize_title,
                     color=text_color, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.5", facecolor=outcome_color,
                               alpha=0.9, edgecolor=edge_color, linewidth=2))

            # Clean up plot with bolder elements
            ax2.set_ylabel('Amount ($)', fontsize=fontsize_labels, fontweight='bold')
            ax2.set_title('Insurance Pool Results', fontsize=fontsize_title, fontweight='bold')
            ax2.grid(axis='y', alpha=0.4, linestyle='--', linewidth=1.5)

            # Make axis lines thicker for better visibility
            ax2.spines['bottom'].set_linewidth(linewidth)
            ax2.spines['left'].set_linewidth(linewidth)
            ax2.tick_params(width=linewidth - 1, length=10)

            # Calculate expected maximum loss for consistent y-axis
            p = accident_probability
            n = num_policyholders
            max_expected_claims = n * p + 2.576 * np.sqrt(n * p * (1 - p)) + 0.5
            max_expected_loss = max_expected_claims * CLAIM_AMOUNT
            y_max = max(max_expected_loss, total_losses) * 1.1
            ax2.set_ylim(0, y_max)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

            # Add a key insight box with formula at the bottom of the plot
            insight_text = f"Key Insight: More policyholders = more stable results\nActual/Expected Ratio = {pool_performance:.2f}"
            props = dict(boxstyle='round', facecolor='#F8F9FA', alpha=0.9,
                         edgecolor='#BDC3C7', linewidth=2)

            fig.text(0.5, 0.02, insight_text, fontsize=fontsize_annotations,
                     ha='center', va='bottom', fontweight='bold', bbox=props)

            # Adjust the layout with generous spacing
            fig.tight_layout()
            fig.subplots_adjust(hspace=0.6, bottom=0.08, top=0.92)

        else:
            # Original layout for desktop
            fig = Figure(figsize=(14, 7))

            # Create subplots side by side
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            # Use more points for display on desktop
            display_n = min(50, num_policyholders)

            # Plot 1: Individual outcomes with improved visualization
            # Blue bar chart for individual outcomes
            ax1.bar(
                ['Without Insurance'],
                [CLAIM_AMOUNT],
                color='lightblue',
                alpha=0.3,
                width=0.6,
                label='Potential loss amount'
            )

            # Overlay scatter plot showing actual outcomes
            x_positions = np.ones(display_n) * 0  # All points at x=0 ("Without Insurance")
            y_positions = individual_costs[:display_n]  # Each person's actual outcome

            # Add jitter to x positions for better visualization
            x_jitter = np.random.uniform(-0.2, 0.2, size=display_n)
            x_positions += x_jitter

            # Plot the actual outcomes as scatter points
            ax1.scatter(
                x_positions,
                y_positions,
                color='blue',
                alpha=0.7,
                s=50,
                label=f'Individual outcomes (n={display_n})'
            )

            # Add a bar for premium with insurance
            ax1.bar(
                ['With Insurance'],
                [fair_premium],
                color='green',
                alpha=0.7,
                width=0.6,
                label='Insurance premium'
            )

            # Original annotations
            ax1.annotate(
                f"{num_with_loss} out of {num_policyholders} people\nexperienced a ${CLAIM_AMOUNT:,} loss",
                xy=(0, CLAIM_AMOUNT / 2),
                xytext=(0, CLAIM_AMOUNT * 0.7),
                ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8)
            )

            # Annotation explaining insurance premium
            ax1.annotate(
                f"Everyone pays\n${fair_premium:,.0f}",
                xy=(1, fair_premium / 2),
                xytext=(1, fair_premium * 1.5),
                ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.8)
            )

            ax1.legend(loc='upper center')

            ax1.set_ylabel('Cost ($)')
            ax1.set_title(f'Individual vs Pooled Outcomes')
            ax1.grid(axis='y', alpha=0.3)

            # Set y-axis limit to ensure visibility of premium
            ax1.set_ylim(0, CLAIM_AMOUNT * 1.1)

            # Format y-axis with dollar signs
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

            # Plot 2: Pooled outcome (insurer perspective)
            ax2.bar(['Premiums', 'Losses'],
                    [pool_premium_total, total_losses],
                    color=['green', 'blue'], alpha=0.7)
            ax2.set_ylabel('Amount ($)')
            ax2.set_title(f"Insurer's Perspective")

            # Calculate expected maximum loss at 99% confidence level based on binomial distribution
            # This helps keep the y-axis consistent across different simulations
            p = accident_probability
            n = num_policyholders
            # Using normal approximation to binomial with continuity correction for 99% CI (2.576 is z-score for 99%)
            max_expected_claims = n * p + 2.576 * np.sqrt(n * p * (1 - p)) + 0.5
            max_expected_loss = max_expected_claims * CLAIM_AMOUNT

            # Set y-axis to use the consistent 99% CI maximum
            y_max = max(max_expected_loss, total_losses) * 1.1  # Add 10% margin
            ax2.set_ylim(0, y_max)

            ax2.grid(True, alpha=0.3)

            # Format y-axis with dollar signs
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

            # Original format
            performance_text = "Surplus" if pool_performance < 1 else "Deficit"
            performance_color = "green" if pool_performance < 1 else "red"

            ax2.text(0.5, 0.95,
                     f"Expected losses: ${pool_premium_total:,.0f}\nActual losses: ${total_losses:,.0f}\n{performance_text}: ${abs(pool_premium_total - total_losses):,.0f}",
                     transform=ax2.transAxes, ha='center', va='top',
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.8))

            # Add annotation for ratio
            ax2.text(1, total_losses + 0.05 * max(pool_premium_total, total_losses),
                     f"Actual/Expected: {pool_performance:.2f}", ha='center', color=performance_color)

            # Adjust layout
            fig.tight_layout()

        # Return the figure and key statistics
        stats = {
            'num_with_loss': num_with_loss,
            'percent_with_loss': percent_with_loss,
            'fair_premium': fair_premium,
            'total_losses': total_losses,
            'pool_premium_total': pool_premium_total,
            'pool_performance': pool_performance,
            'seed': seed  # Include seed in stats
        }

        return fig, stats

    # Original function for compatibility
    else:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

        # Rest of the implementation would be similar to the return_fig=True case
        plt.show()

        # Print statistics
        print("\nInsurance Interpretation:")
        print(f"• Individual Risk: Each person has a {accident_probability:.1%} chance of a ${CLAIM_AMOUNT:,.0f} loss.")
        print(
            f"• Without Insurance: {num_with_loss} people ({percent_with_loss:.1f}%) faced a ${CLAIM_AMOUNT:,.0f} loss.")
        print(f"• With Insurance: Everyone pays a premium of ${fair_premium:.0f}.")
        print(f"• Risk Pooling Result: The insurer collected ${pool_premium_total:,.0f} and paid ${total_losses:,.0f}.")