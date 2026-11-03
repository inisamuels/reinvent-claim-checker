# Rule for "Confirmed"

A claim is **confirmed** only if all three answers are yes.

1. Is the source page on aws.amazon.com?
2. Is the quote copied exactly from that page?
3. Does the quote back every fact in the claim?

Any "no" means the claim is **rejected**, with a one-line reason.

## Agents

| Role | Does |
|---|---|
| Lead agent | Hands out each claim and builds the final page |
| Researcher | Finds the aws.amazon.com page and copies the sentences, or reports no match |
| Fact checker | Runs the 3 checks and returns confirmed or rejected, with a reason |