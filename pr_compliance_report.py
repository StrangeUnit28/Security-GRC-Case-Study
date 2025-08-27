
import matplotlib.pyplot as plt
from datetime import datetime
from checks_prs import get_pr_approval_status
from fpdf import FPDF


def generate_report(compliant, violations):
    total = len(compliant) + len(violations)
    percent_compliant = (len(compliant) / total * 100) if total else 0
    percent_violations = (len(violations) / total * 100) if total else 0

    # Pie chart
    labels = ['Compliant PRs', 'Violations']
    sizes = [len(compliant), len(violations)]
    colors = ['#4CAF50', '#F44336']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    plt.title('PR Approval Compliance')
    chart_path = 'pr_compliance_pie.png'
    plt.savefig(chart_path)
    plt.close()

    # PDF report
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'PR Approval Compliance Report', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Generated at: {now}', ln=True)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Summary', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f'Total merged PRs: {total}', ln=True)
    pdf.cell(0, 8, f'Compliant PRs: {len(compliant)} ({percent_compliant:.1f}%)', ln=True)
    pdf.cell(0, 8, f'Violations: {len(violations)} ({percent_violations:.1f}%)', ln=True)
    pdf.ln(5)
    pdf.image(chart_path, x=pdf.get_x(), y=pdf.get_y(), w=100)
    pdf.ln(60)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Violations', ln=True)
    pdf.set_font('Arial', '', 12)
    if violations:
        for pr in violations:
            pdf.multi_cell(0, 8, f"PR #{pr['number']} ({pr['title']}) by {pr['user']['login']} merged at {pr['merged_at']}")
    else:
        pdf.cell(0, 8, 'None', ln=True)
    pdf.output('pr_compliance_report.pdf')
    print('Report generated: pr_compliance_report.pdf')

if __name__ == "__main__":
    compliant, violations = get_pr_approval_status()
    generate_report(compliant, violations)
