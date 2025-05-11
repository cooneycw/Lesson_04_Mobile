import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from scipy.stats import lognorm


def demonstrate_driver_comparison(base_frequency=0.05, base_severity=8000, bad_driver_freq_multiplier=3.0,
                                  bad_driver_severity_multiplier=2.0, seed=42, return_fig=False,
                                  good_driver_image="drake.jpeg", is_mobile=False):
    """
    Demonstrates the difference in outcomes between driver cohorts

    Parameters:
    -----------
    base_frequency : float
        Base accident frequency for first cohort
    base_severity : float
        Base accident severity for first cohort
    bad_driver_freq_multiplier : float
        How much more frequently second cohort has accidents
    bad_driver_severity_multiplier : float
        How much more severe second cohort's accidents are
    seed : int
        Random seed for reproducibility
    return_fig : bool
        If True, returns the figure and stats for Shiny integration
    good_driver_image : str
        Image filename to use for the first cohort (either "drake.jpeg" or "kendrick.jpeg")
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

    # Set random seed for reproducibility
    np.random.seed(seed)

    # Extract driver names from image filename
    good_driver_name = good_driver_image.split('.')[0].capitalize()
    bad_driver_name = "Kendrick" if good_driver_name == "Drake" else "Drake"

    # Use specific cohort names
    first_cohort_name = f"{good_driver_name} Cohort"
    second_cohort_name = f"{bad_driver_name} Cohort"

    # Define parameters for each driver type
    second_cohort_frequency = base_frequency * bad_driver_freq_multiplier
    second_cohort_severity = base_severity * bad_driver_severity_multiplier

    # Number of drivers to simulate - reduce for mobile
    if is_mobile:
        num_first_cohort = 80  # Further reduced for mobile
        num_second_cohort = 80
    else:
        num_first_cohort = 200
        num_second_cohort = 200

    # Parameters for lognormal distribution
    first_sigma = 0.4  # Smaller sigma for first cohort (less variance)
    second_sigma = 0.6  # Larger sigma for second cohort (more variance)

    # Calculate mu so that the median of the lognormal is our target severity
    first_mu = np.log(base_severity) - 0.5 * first_sigma ** 2
    second_mu = np.log(second_cohort_severity) - 0.5 * second_sigma ** 2

    # Generate individual driver frequencies
    first_cohort_frequencies = np.random.normal(base_frequency, base_frequency * 0.3, num_first_cohort)
    first_cohort_frequencies = np.maximum(first_cohort_frequencies, 0.001)  # Minimum 0.1% frequency

    second_cohort_frequencies = np.random.normal(second_cohort_frequency, second_cohort_frequency * 0.3,
                                                 num_second_cohort)
    second_cohort_frequencies = np.maximum(second_cohort_frequencies, 0.001)  # Minimum 0.1% frequency

    # Generate individual driver severities (using lognormal)
    first_cohort_severities = lognorm.rvs(first_sigma, scale=np.exp(first_mu), size=num_first_cohort)
    second_cohort_severities = lognorm.rvs(second_sigma, scale=np.exp(second_mu), size=num_second_cohort)

    # Calculate statistics
    first_avg_frequency = np.mean(first_cohort_frequencies)
    second_avg_frequency = np.mean(second_cohort_frequencies)

    first_avg_severity = np.mean(first_cohort_severities)
    second_avg_severity = np.mean(second_cohort_severities)

    first_total_losses = first_avg_frequency * first_avg_severity * num_first_cohort
    second_total_losses = second_avg_frequency * second_avg_severity * num_second_cohort

    # For Shiny integration
    if return_fig:
        # Create figure with adjusted size based on mobile or desktop view
        if is_mobile:
            # Use a taller figure for mobile and scrolling
            fig = Figure(figsize=(9, 14))
        else:
            fig = Figure(figsize=(10.5, 10))

        # Create subplot - simplify to just one plot
        ax1 = fig.add_subplot(111)  # Main scatterplot

        # Plot: Scatter plot of driver risk profiles
        # Add small jitter to separate overlapping points
        jitter_x_first = np.random.normal(0, 0.001, num_first_cohort)
        jitter_x_second = np.random.normal(0, 0.001, num_second_cohort)

        # Point size - larger for mobile to be more touch-friendly
        point_size = 80 if is_mobile else 70

        # Scatter plot for first cohort - brighter colors for mobile
        if is_mobile:
            first_color = '#2ECC71'  # Bright green
            second_color = '#E74C3C'  # Bright red
            first_edge = '#27AE60'  # Darker green edge
            second_edge = '#C0392B'  # Darker red edge
            alpha = 0.8  # More opaque for mobile
        else:
            first_color = 'green'
            second_color = 'red'
            first_edge = 'darkgreen'
            second_edge = 'darkred'
            alpha = 0.7

        ax1.scatter(
            first_cohort_frequencies + jitter_x_first,
            first_cohort_severities,
            color=first_color,
            alpha=alpha,
            s=point_size,
            label=f'{first_cohort_name}',
            edgecolors=first_edge
        )

        # Scatter plot for second cohort
        ax1.scatter(
            second_cohort_frequencies + jitter_x_second,
            second_cohort_severities,
            color=second_color,
            alpha=alpha,
            s=point_size,
            label=f'{second_cohort_name}',
            edgecolors=second_edge
        )

        # Add center points for each cluster - make them more prominent
        center_point_size = 200 if is_mobile else 150

        ax1.scatter(
            first_avg_frequency,
            first_avg_severity,
            color=first_edge,
            s=center_point_size,
            marker='*',
            label=f'{first_cohort_name} Avg' if is_mobile else f'{first_cohort_name} Average',
            zorder=5,  # Ensure it's on top
            edgecolors='black'
        )

        ax1.scatter(
            second_avg_frequency,
            second_avg_severity,
            color=second_edge,
            s=center_point_size,
            marker='*',
            label=f'{second_cohort_name} Avg' if is_mobile else f'{second_cohort_name} Average',
            zorder=5,  # Ensure it's on top
            edgecolors='black'
        )

        # Special version for mobile - make everything very clear
        if is_mobile:
            # Make the grid more visible but not distracting
            ax1.grid(True, alpha=0.5, linewidth=1.5, linestyle='--')

            # Make axis lines thicker for better visibility
            ax1.spines['bottom'].set_linewidth(2)
            ax1.spines['left'].set_linewidth(2)
            ax1.tick_params(width=2)

            # Just show the key average lines with thicker lines
            ax1.axvline(x=first_avg_frequency, color='lightgreen', linestyle='--', alpha=0.7, linewidth=2)
            ax1.axvline(x=second_avg_frequency, color='lightcoral', linestyle='--', alpha=0.7, linewidth=2)

            # Bolder text for readability with background boxes
            ax1.text(first_avg_frequency, ax1.get_ylim()[0] * 1.05,
                     f"{first_cohort_name}\n{first_avg_frequency:.1%}",
                     color='darkgreen', ha='center', va='bottom', rotation=90, fontsize=14,
                     fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, pad=3, boxstyle='round'))

            ax1.text(second_avg_frequency, ax1.get_ylim()[0] * 1.05,
                     f"{second_cohort_name}\n{second_avg_frequency:.1%}",
                     color='darkred', ha='center', va='bottom', rotation=90, fontsize=14,
                     fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, pad=3, boxstyle='round'))
        else:
            # Original reference lines
            ax1.axvline(x=base_frequency, color='lightgreen', linestyle='--', alpha=0.5)
            ax1.axvline(x=second_cohort_frequency, color='lightcoral', linestyle='--', alpha=0.5)

            ax1.axhline(y=base_severity, color='lightgreen', linestyle='--', alpha=0.5)
            ax1.axhline(y=second_cohort_severity, color='lightcoral', linestyle='--', alpha=0.5)

            # Annotations for the lines
            ax1.text(base_frequency, ax1.get_ylim()[0] * 1.05, f"{first_cohort_name} Frequency: {base_frequency:.1%}",
                     color='darkgreen', ha='center', va='bottom', rotation=90)
            ax1.text(second_cohort_frequency, ax1.get_ylim()[0] * 1.05,
                     f"{second_cohort_name} Frequency: {second_cohort_frequency:.1%}",
                     color='darkred', ha='center', va='bottom', rotation=90)

        # Format axes with updated terminology - larger text for mobile
        if is_mobile:
            ax1.set_xlabel('Accident Frequency', fontsize=18, fontweight='bold')
            ax1.set_ylabel('Claim Amount ($)', fontsize=18, fontweight='bold')
            ax1.set_title('Driver Risk Profiles', fontsize=20, fontweight='bold')
        else:
            ax1.set_xlabel('Est. Accident Frequency (probability per year)', fontsize=12)
            ax1.set_ylabel('Est. Average Claim Amount ($)', fontsize=12)
            ax1.set_title('Driver Risk Profiles: Frequency vs Claim Amount', fontsize=14)

        # Move legend to top for better visibility on mobile
        if is_mobile:
            # More prominent legend with larger font
            ax1.legend(fontsize=14, loc='upper center', ncol=2,
                       framealpha=0.9, edgecolor='#BDC3C7', frameon=True)
        else:
            ax1.legend(fontsize=12)

        ax1.grid(True, alpha=0.3)

        # Set x-axis as percentage
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))

        # Set y-axis format to display dollar amounts
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))

        # For desktop only: Add summary statistics in a box
        if not is_mobile:
            summary_text = (
                f"Risk Profile Comparison\n\n"
                f"{first_cohort_name}:\n"
                f"• Avg Frequency: {first_avg_frequency:.1%}\n"
                f"• Avg Claim Amount: ${first_avg_severity:,.0f}\n"
                f"• Total Expected Loss: ${first_total_losses:,.0f}\n\n"
                f"{second_cohort_name}:\n"
                f"• Avg Frequency: {second_avg_frequency:.1%} ({second_avg_frequency / first_avg_frequency:.1f}x higher)\n"
                f"• Avg Claim Amount: ${second_avg_severity:,.0f} ({second_avg_severity / first_avg_severity:.1f}x higher)\n"
                f"• Total Expected Loss: ${second_total_losses:,.0f} ({second_total_losses / first_total_losses:.1f}x higher)"
            )

            # Place text box on the right side (LEFT JUSTIFIED)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
            ax1.text(1.05, 0.5, summary_text, fontsize=12,
                     verticalalignment='center', horizontalalignment='left',
                     bbox=props, transform=ax1.transAxes)

            # Adjust layout to make space for the text box
            fig.tight_layout()
            fig.subplots_adjust(right=0.75)  # Make room for the summary box on the right
        else:
            # For mobile, add direct annotations to the chart
            # Add a summary box at the top of the mobile chart
            summary_box_text = (
                f"Risk Comparison:\n"
                f"• {first_cohort_name}: {first_avg_frequency:.1%} freq, ${first_avg_severity:,.0f} claims\n"
                f"• {second_cohort_name}: {second_avg_frequency:.1%} freq, ${second_avg_severity:,.0f} claims\n"
                f"• Difference: {second_total_losses / first_total_losses:.1f}x higher risk"
            )

            # Place at top of chart
            props = dict(boxstyle='round', facecolor='#F8F9FA', alpha=0.9, ec='#BDC3C7')
            ax1.text(0.5, 0.97, summary_box_text, fontsize=13,
                     transform=ax1.transAxes, ha='center', va='top',
                     bbox=props)

            # Adjust for mobile scrolling with more padding
            fig.tight_layout()
            fig.subplots_adjust(bottom=0.1, top=0.85)  # More space at top and bottom

        # Stats to return
        stats = {
            'good_avg_frequency': first_avg_frequency,
            'bad_avg_frequency': second_avg_frequency,
            'good_avg_severity': first_avg_severity,
            'bad_avg_severity': second_avg_severity,
            'good_total_losses': first_total_losses,
            'bad_total_losses': second_total_losses,
            'loss_multiplier': second_total_losses / first_total_losses,
            'freq_multiplier': second_avg_frequency / first_avg_frequency,
            'severity_multiplier': second_avg_severity / first_avg_severity,
            'good_driver_image': good_driver_image,
            'good_driver_name': good_driver_name,
            'bad_driver_name': bad_driver_name,
            'first_cohort_name': first_cohort_name,
            'second_cohort_name': second_cohort_name
        }

        return fig, stats

    # Original function for compatibility
    else:
        # Create figure
        fig = plt.figure(figsize=(14, 10))

        # Rest of the implementation would be similar to the return_fig=True case
        plt.show()

        # Print statistics
        print("\nDriver Comparison Interpretation:")
        print(
            f"• {first_cohort_name}: {first_avg_frequency:.1%} accident rate, ${first_avg_severity:,.2f} avg severity")
        print(
            f"• {second_cohort_name}: {second_avg_frequency:.1%} accident rate, ${second_avg_severity:,.2f} avg severity")
        print(f"• {first_cohort_name} total loss: ${first_total_losses:,.0f}")
        print(
            f"• {second_cohort_name} total loss: ${second_total_losses:,.0f} ({second_total_losses / first_total_losses:.1f}x higher)")