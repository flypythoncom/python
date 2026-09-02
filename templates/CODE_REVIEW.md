# Code review

- Does the change satisfy the user contract and preserve unrelated behavior?
- Are boundary inputs, errors, timeouts, and retries explicit?
- Are secrets, permissions, destructive effects, and model/tool calls safe?
- Do tests prove the reported failure, success, and important edge cases?
- Is the diff smaller and clearer than plausible alternatives?
- Was real runtime behavior checked where unit tests are insufficient?
