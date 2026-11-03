# Hand checks

Checked by hand against the AWS Official Source Snapshot (captured 3 November 2025) and the re:Invent Candidate Items CSV, using the three questions in `confirm_rule.md`.

## C-01
- Claim: "Amazon Bedrock AgentCore is now generally available for building and running AI agents at scale."
- Source page: https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available/ (snapshot entry AWS-SRC-019)
- Quote: "Amazon Bedrock AgentCore is now generally available. AgentCore is an agentic platform to build, deploy and operate AI agents securely at scale, using any framework and any foundation model."
- 1. Is the source page on aws.amazon.com? yes
- 2. Is the quote copied exactly from that page? yes
- 3. Does the quote back every fact in the claim? yes
- Result: confirmed

## C-05
- Claim: "Amazon S3 Vectors is now GA and lets you store and query vector embeddings natively in S3 at massive scale."
- Source page: https://aws.amazon.com/s3/features/vectors/ (snapshot entry AWS-SRC-015)
- Quote: "Amazon S3 Vectors is in preview and is available in five AWS Regions."
- 1. Is the source page on aws.amazon.com? yes
- 2. Is the quote copied exactly from that page? yes
- 3. Does the quote back every fact in the claim? no
- Result: rejected. Quote says S3 Vectors is in preview, not generally available.