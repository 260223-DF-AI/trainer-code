# LLM Security Considerations

## Learning Objectives

- Identify security risks specific to LLM usage in professional environments
- Understand data privacy implications of different LLM access methods
- Apply API key management best practices
- Evaluate LLM tools based on security and compliance requirements

## Why This Matters

When you use an LLM, your prompts and data are typically sent to an external server. For data professionals who work with sensitive datasets, credentials, and proprietary business logic, understanding the security implications of LLM usage is critical. A single careless prompt can expose production database credentials or customer PII.

## The Concept

### Data Privacy by Access Method

Different ways of accessing LLMs carry different privacy implications:

| Access Method | Data Handling | Privacy Level |
| ------------- | ------------- | ------------- |
| Web chat (free tier) | May be used for training | Low |
| API (paid tier) | Typically not used for training | Medium |
| Enterprise plan | Strict data isolation, no training | High |
| Self-hosted (Llama) | Data never leaves your infrastructure | Highest |

**Always check the terms of service** for any AI tool you use. Key questions:

1. Is my data used to train the model?
2. How long is my data retained?
3. Who has access to my prompts and responses?
4. Is data encrypted in transit and at rest?
5. What jurisdiction stores the data?

### API Key Management

LLM APIs require authentication keys. These keys are sensitive credentials:

#### Do Not

```python
# UNSAFE: API key hardcoded in source code
import openai
client = openai.Client(api_key="sk-abc123def456...")

# UNSAFE: API key in a config file committed to git
config = {
    "openai_key": "sk-abc123def456..."
}
```

#### Do

```python
# SAFE: API key from environment variable
import os
import openai

client = openai.Client(
    api_key=os.environ.get("OPENAI_API_KEY")
)
```

```bash
# Set environment variable (do not commit .env to git)
export OPENAI_API_KEY="sk-abc123def456..."
```

```gitignore
# .gitignore - always exclude credential files
.env
*.key
credentials.json
```

#### Additional API Key Best Practices

- **Rotate keys regularly** -- especially if team members leave
- **Use separate keys** for development and production
- **Set spending limits** on API accounts to prevent runaway costs
- **Monitor usage** -- unexpected spikes may indicate key compromise
- **Use service accounts** rather than personal keys for production

### What Not to Share with LLMs

Create a mental checklist before pasting anything into an AI tool:

| Category | Examples | Risk |
| -------- | -------- | ---- |
| Credentials | Database passwords, API keys, tokens | Direct system access |
| PII | Customer names, emails, SSNs | Privacy violation, legal liability |
| Proprietary code | Trade secret algorithms, business logic | Competitive exposure |
| Infrastructure details | Server IPs, network topology | Attack surface exposure |
| Financial data | Revenue figures, salary data | Regulatory violation |

#### Safe Alternatives

Instead of sharing sensitive data, use anonymization:

```
UNSAFE:
"Debug this connection error:
postgresql://admin:P@ssw0rd@10.0.1.50:5432/prod_customers"

SAFE:
"Debug this PostgreSQL connection error:
postgresql://[user]:[pass]@[host]:5432/[database]
Error: Connection refused"
```

### Enterprise LLM Security Features

Enterprise-grade AI tools typically offer:

- **Data isolation**: Your data is not mixed with other customers' data
- **No training on customer data**: Your prompts are not used to improve the model
- **SOC 2 compliance**: Audited security controls
- **SSO integration**: Single sign-on with your organization's identity provider
- **Audit logs**: Record of all AI interactions
- **Data residency**: Control over where data is processed geographically

### Evaluating LLM Tools for Security

When your team evaluates an AI tool, consider:

```
Security Evaluation Checklist:
[ ] What is the data retention policy?
[ ] Is data used for model training?
[ ] Is the service SOC 2 / ISO 27001 certified?
[ ] Does it support SSO and MFA?
[ ] Can we set up audit logging?
[ ] Where is data processed (geography)?
[ ] What is the incident response process?
[ ] Can we use a self-hosted option?
```

### Organizational Policies

Effective AI security requires clear organizational policies:

1. **Approved tools list** -- which AI tools are sanctioned for use
2. **Data classification** -- what data can be shared, what cannot
3. **Usage guidelines** -- how to anonymize data before sharing
4. **Incident reporting** -- what to do if sensitive data is accidentally shared
5. **Training requirements** -- mandatory AI security training for all team members

## Key Takeaways

- Different LLM access methods have different data privacy guarantees
- Never share credentials, PII, or proprietary code with AI tools
- API keys are sensitive credentials that require proper management
- Enterprise LLM plans offer stronger security controls
- Organizations need clear policies governing AI tool usage

## Additional Resources

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OpenAI - Data Usage Policies](https://openai.com/policies/usage-policies)
- [Anthropic - Security Practices](https://www.anthropic.com/security)
