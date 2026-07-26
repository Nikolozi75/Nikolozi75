import streamlit as st
import re
import json
from datetime import datetime
import os

# Page Configuration
st.set_page_config(
    page_title="SecureGuard Audit Tool", page_icon="🛡️", layout="wide"
)

st.title("🛡️ Digital Security & Credential Auditor")
st.write(
    "Evaluate your organization's password strength and review essential"
    " cybersecurity checklists."
)

# Sidebar Navigation
option = st.sidebar.selectbox(
    "Select Tool", ["Password Policy Audit", "Security Checklist Generator", "Export Reports"]
)

# ============================================================================
# SECTION 1: Password Policy Audit (Enhanced)
# ============================================================================
if option == "Password Policy Audit":
    st.header("🔐 Corporate Password Strength Checker")
    
    user_password = st.text_input(
        "Enter a sample password to test against guidelines:", type="password"
    )

    if user_password:
        score = 0
        max_score = 10
        feedback = []
        
        # Length Check
        if len(user_password) >= 16:
            score += 3
            feedback.append("✔️ Excellent length (16+ characters).")
        elif len(user_password) >= 12:
            score += 2
            feedback.append("✔️ Good length (12-15 characters).")
        else:
            feedback.append("❌ Password is too short (aim for 12+ characters, 16+ is best).")

        # Uppercase Check
        if re.search(r'[A-Z]', user_password):
            score += 2
            feedback.append("✔️ Contains uppercase letters.")
        else:
            feedback.append("❌ Missing uppercase letters (A-Z).")

        # Lowercase Check
        if re.search(r'[a-z]', user_password):
            score += 2
            feedback.append("✔️ Contains lowercase letters.")
        else:
            feedback.append("❌ Missing lowercase letters (a-z).")

        # Numbers Check
        if re.search(r'[0-9]', user_password):
            score += 2
            feedback.append("✔️ Contains numbers.")
        else:
            feedback.append("❌ Missing numbers (0-9).")

        # Special Characters Check
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', user_password):
            score += 1
            feedback.append("✔️ Contains special characters.")
        else:
            feedback.append("❌ Missing special characters (!@#$%^&*, etc).")

        # Common Patterns Check
        common_patterns = ['123', 'abc', 'password', 'qwerty', 'admin', '000', '111']
        if not any(pattern in user_password.lower() for pattern in common_patterns):
            score += 0  # No bonus, just avoid penalty
            feedback.append("✔️ No obvious patterns detected.")
        else:
            feedback.append("⚠️ Contains common patterns (consider changing).")
            score = max(0, score - 1)

        # Calculate strength percentage
        strength_percentage = (score / max_score) * 100

        # Display Results with Progress Bar
        col1, col2 = st.columns([2, 1])
        with col1:
            st.progress(strength_percentage / 100)
        with col2:
            if strength_percentage >= 80:
                st.success(f"Strong: {score}/{max_score}")
            elif strength_percentage >= 60:
                st.warning(f"Moderate: {score}/{max_score}")
            else:
                st.error(f"Weak: {score}/{max_score}")

        st.write("### Feedback:")
        for item in feedback:
            st.write(item)

        # Recommendations
        st.write("### 💡 Recommendations:")
        recommendations = [
            "Use at least 16 characters for critical accounts",
            "Avoid dictionary words and personal information",
            "Use a passphrase or password manager for complex passwords",
            "Never reuse passwords across different services",
            "Change passwords immediately if compromised"
        ]
        for rec in recommendations:
            st.write(f"• {rec}")


# ============================================================================
# SECTION 2: Security Checklist Generator (Enhanced & Dynamic)
# ============================================================================
elif option == "Security Checklist Generator":
    st.header("📋 Custom Security Checklist")
    
    business_type = st.selectbox(
        "Select your business type:",
        ["General", "Small Business", "Healthcare", "FinTech", "E-commerce", "SaaS", "Custom"]
    )

    company_name = st.text_input("Enter your company name:")

    # Define checklists for different business types
    checklists = {
        "General": {
            "Access Control": [
                "Enforce Two-Factor Authentication (2FA) on all admin accounts",
                "Implement role-based access control (RBAC)",
                "Review and remove inactive user accounts regularly"
            ],
            "Software & Infrastructure": [
                "Regularly update software and dependencies",
                "Patch operating systems and third-party applications",
                "Use firewalls and intrusion detection systems"
            ],
            "Training & Awareness": [
                "Conduct basic security awareness training for staff",
                "Schedule quarterly phishing awareness simulations",
                "Document security policies and share with all employees"
            ]
        },
        "Small Business": {
            "Access Control": [
                "Enable 2FA on all employee accounts",
                "Use a password manager (1Password, Bitwarden, etc.)",
                "Limit admin privileges to authorized personnel only"
            ],
            "Data Protection": [
                "Encrypt sensitive data at rest and in transit",
                "Regular automated backups (at least daily)",
                "Establish data retention and deletion policies"
            ],
            "Software & Infrastructure": [
                "Keep all software and systems updated",
                "Disable unnecessary services and ports",
                "Monitor for suspicious network activity"
            ],
            "Training & Awareness": [
                "Train employees on phishing attacks",
                "Establish incident response procedures",
                "Create written security policies"
            ]
        },
        "Healthcare": {
            "Compliance": [
                "Ensure HIPAA compliance for all patient data",
                "Conduct annual security risk assessments",
                "Maintain audit logs for all data access"
            ],
            "Access Control": [
                "Implement strong authentication for EHR systems",
                "Use role-based access for different staff roles",
                "Require password changes every 90 days"
            ],
            "Data Protection": [
                "Encrypt all patient records (PII/PHI)",
                "Use secure communication channels for patient data",
                "Establish incident reporting procedures"
            ],
            "Training & Awareness": [
                "Annual HIPAA training for all staff",
                "Train on handling sensitive patient information",
                "Document security incidents and responses"
            ]
        },
        "FinTech": {
            "Compliance": [
                "Maintain PCI DSS compliance",
                "Regular third-party security audits",
                "Implement fraud detection systems"
            ],
            "Access Control": [
                "Multi-factor authentication for all accounts",
                "Implement API key rotation policies",
                "Zero-trust network access controls"
            ],
            "Data Protection": [
                "End-to-end encryption for all transactions",
                "Tokenization of sensitive financial data",
                "Implement rate limiting and DDoS protection"
            ],
            "Training & Awareness": [
                "Regular security training for developers",
                "Conduct penetration testing quarterly",
                "Maintain incident response playbooks"
            ]
        },
        "E-commerce": {
            "Payment Security": [
                "Implement PCI DSS compliance",
                "Use secure payment gateways (Stripe, PayPal)",
                "Never store full credit card numbers"
            ],
            "Customer Data": [
                "Encrypt customer personal information",
                "Implement secure login and password reset",
                "Regular security updates for web applications"
            ],
            "Infrastructure": [
                "Use HTTPS/SSL certificates on all pages",
                "Regular security scanning and penetration testing",
                "Implement Web Application Firewall (WAF)"
            ],
            "Training & Awareness": [
                "Train staff on handling customer data securely",
                "Monitor for suspicious transactions",
                "Create transparent privacy policies"
            ]
        },
        "SaaS": {
            "Cloud Security": [
                "Implement cloud security best practices",
                "Use Infrastructure-as-Code for configuration management",
                "Regular cloud resource auditing"
            ],
            "API Security": [
                "Implement API authentication and authorization",
                "Rate limiting and request validation",
                "API key rotation and management"
            ],
            "Data Protection": [
                "Encrypt data in transit (TLS/SSL)",
                "Encrypt sensitive data at rest",
                "Implement database access controls"
            ],
            "Compliance & Monitoring": [
                "SOC 2 Type II compliance",
                "Continuous security monitoring",
                "Regular vulnerability assessments"
            ]
        }
    }

    if company_name:
        selected_checklist = checklists.get(business_type, checklists["General"])
        
        st.success(f"✅ Security Plan for: **{company_name}** ({business_type})")
        st.write("---")

        # Create session state for checklist tracking
        if 'checklist_state' not in st.session_state:
            st.session_state.checklist_state = {}

        completed_count = 0
        total_count = 0

        for category, items in selected_checklist.items():
            st.subheader(f"📌 {category}")
            
            for idx, item in enumerate(items):
                item_key = f"{business_type}_{category}_{idx}"
                total_count += 1
                
                is_checked = st.checkbox(item, key=item_key)
                
                if is_checked:
                    completed_count += 1
                    st.session_state.checklist_state[item_key] = True
        
        # Progress Summary
        st.write("---")
        progress_percentage = (completed_count / total_count * 100) if total_count > 0 else 0
        st.write(f"### 📊 Completion Status: {completed_count}/{total_count} ({progress_percentage:.0f}%)")
        st.progress(progress_percentage / 100)

        # Export button
        if st.button("📥 Download Checklist as JSON"):
            checklist_data = {
                "company": company_name,
                "business_type": business_type,
                "generated_date": datetime.now().isoformat(),
                "completion_percentage": progress_percentage,
                "checklist": selected_checklist
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(checklist_data, indent=2),
                file_name=f"{company_name}_security_checklist.json",
                mime="application/json"
            )


# ============================================================================
# SECTION 3: Export Reports
# ============================================================================
elif option == "Export Reports":
    st.header("📊 Security Audit Reports")
    
    st.write("### Generate and Export Your Security Audit")
    
    report_type = st.selectbox(
        "Select report type:",
        ["Password Strength Summary", "Compliance Checklist", "Executive Summary"]
    )

    if report_type == "Password Strength Summary":
        st.info("Run the Password Audit tool first, then return here to export results.")
        if st.button("Generate Password Report"):
            report_content = """
# Password Strength Audit Report

**Generated:** {date}

## Security Standards
- Minimum length: 12 characters (16+ recommended)
- Required: Uppercase, lowercase, numbers, special characters
- Avoid: Common patterns and dictionary words

## Best Practices
1. Use unique passwords for each service
2. Implement password managers
3. Enable multi-factor authentication
4. Review passwords quarterly
""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            st.download_button(
                label="📄 Download Report",
                data=report_content,
                file_name="password_audit_report.txt",
                mime="text/plain"
            )

    elif report_type == "Compliance Checklist":
        compliance_framework = st.selectbox(
            "Select framework:",
            ["NIST Cybersecurity Framework", "ISO 27001", "CIS Controls", "OWASP Top 10"]
        )
        
        if st.button("Generate Compliance Report"):
            report_content = f"""
# Compliance Report: {compliance_framework}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Framework: {compliance_framework}

This report outlines the security requirements based on the selected framework.

### Key Areas:
- Asset Management
- Access Control
- Data Protection
- Incident Response
- Vendor Management

Please review your current controls against these requirements.
"""
            st.download_button(
                label="📄 Download Report",
                data=report_content,
                file_name=f"compliance_report_{compliance_framework.replace(' ', '_')}.txt",
                mime="text/plain"
            )

    elif report_type == "Executive Summary":
        if st.button("Generate Executive Summary"):
            report_content = f"""
# Executive Security Summary

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview
This summary provides a high-level view of your organization's security posture.

## Key Metrics
- Password Strength: To be completed
- Compliance Status: To be completed
- Risk Level: Medium (requires assessment)

## Recommendations
1. Implement multi-factor authentication (MFA) organization-wide
2. Conduct regular security awareness training
3. Perform quarterly security assessments
4. Establish an incident response plan
5. Review and update access controls regularly

## Next Steps
- Schedule a detailed security audit
- Engage with IT security team
- Allocate resources for security improvements
"""
            st.download_button(
                label="📄 Download Summary",
                data=report_content,
                file_name="executive_security_summary.txt",
                mime="text/plain"
            )

st.write("---")
st.write(
    "💡 **Pro Tip:** Use this tool to establish baseline security standards and track improvements over time."
)
