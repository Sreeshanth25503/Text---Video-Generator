# Security Policy

## Reporting Security Issues

**Do not** create a public GitHub issue for security vulnerabilities.

Instead, please report to: [your-email@example.com](mailto:your-email@example.com)

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We will acknowledge your report within 48 hours and work on a fix.

## Supported Versions

| Version | Status      |
| ------- | ----------- |
| Latest  | Supported   |
| Older   | Best effort |

## Dependencies

This project uses:

- PyTorch (Facebook Research)
- Diffusers (Hugging Face)
- Gradio (Gradio)

For security updates in these libraries, keep them updated:

```bash
pip install --upgrade -r requirements.txt
```

## Security Best Practices

When using this project:

1. Keep dependencies updated
2. Use in secure environment
3. Don't share API keys or credentials
4. Verify model sources

Thank you for helping keep this project secure!
