import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


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
        # Create figure with mobile-optimized size if needed
        if is_mobile:
            # For mobile, use a vertically stacked layout
            fig = Figure(figsize=(6, 10))

            # Create subplots stacked vertically
            ax1 = fig.add_subplot(211)  # Top plot
            ax2 = fig.add_subplot(212)  # Bottom plot

            # Increase font sizes for mobile
            plt.rcParams.update({'font.size': 10})

            # Use fewer points for display on mobile
            display_n = min(25, num_policyholders)
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
            s=30 if is_mobile else 50,  # Smaller points on mobile
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

        # Simplified annotations for mobile
        if is_mobile:
            # Simpler annotation showing how many people experienced a loss
            ax1.annotate(
                f"{num_with_loss}/{num_policyholders}\nhad ${CLAIM_AMOUNT:,} loss",
                xy=(0, CLAIM_AMOUNT / 2),
                xytext=(0, CLAIM_AMOUNT * 0.65),
                ha='center',
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="lightblue", alpha=0.8)
            )

            # Simpler annotation explaining insurance premium
            ax1.annotate(
                f"Premium:\n${fair_premium:,.0f}",
                xy=(1, fair_premium / 2),
                xytext=(1, fair_premium * 1.5),
                ha='center',
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="lightgreen", alpha=0.8)
            )

            # Only show "Premium Outcomes" label in the legend
            handles, labels = ax1.get_legend_handles_labels()
            ax1.legend([handles[2]], [labels[2]], loc='upper center', fontsize=9)
        else:
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
        ax2.bar(['Premiums', 'Losses'],  # Shorter labels for mobile
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

        # Simplified annotation for mobile
        performance_text = "Surplus" if pool_performance < 1 else "Deficit"
        performance_color = "green" if pool_performance < 1 else "red"

        if is_mobile:
            ax2.text(0.5, 0.95,
                     f"Expected: ${pool_premium_total:,.0f}\nActual: ${total_losses:,.0f}\n{performance_text}: ${abs(pool_premium_total - total_losses):,.0f}",
                     transform=ax2.transAxes, ha='center', va='top', fontsize=9,
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))

            # Add ratio to bar
            ax2.text(1, total_losses + 0.03 * max(pool_premium_total, total_losses),
                     f"A/E: {pool_performance:.2f}", ha='center', color=performance_color, fontsize=9)
        else:
            ax2.text(0.5, 0.95,
                     f"Expected losses: ${pool_premium_total:,.0f}\nActual losses: ${total_losses:,.0f}\n{performance_text}: ${abs(pool_premium_total - total_losses):,.0f}",
                     transform=ax2.transAxes, ha='center', va='top',
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.8))

            # Add annotation for ratio
            ax2.text(1, total_losses + 0.05 * max(pool_premium_total, total_losses),
                     f"Actual/Expected: {pool_performance:.2f}", ha='center', color=performance_color)

        # Adjust layout
        fig.tight_layout()

        # More spacing between subplots for mobile
        if is_mobile:
            fig.subplots_adjust(hspace=0.5)

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