🚀 Canvas-Driven Development Method - Complete Workflow

1. Understand Core Philosophy: Canvas whiteboard as single source of truth, code is its serialized form; graphical language superior to text description; humans responsible for architecture design, AI responsible for code implementation
/
2. Prepare Tool Environment: Install Obsidian (free open-source whiteboard tool); Configure AI assistant (Claude/GPT-4, must support reading Canvas JSON format); Prepare target project codebase
/
3. Generate Initial Architecture Whiteboard: Provide project code path to AI; Use architecture analysis prompt to have AI scan project structure; AI automatically generates .canvas file containing module nodes and dependency connections
/
4. Open .canvas File in Obsidian: Import generated architecture whiteboard; Check auto-identified modules, files, API call relationships; Verify key dependency connections are accurate
/
5. Manually Optimize Whiteboard Architecture: Drag and adjust module positions for clear layout; Add implicit dependency connections AI missed; Add annotation nodes to mark key design decisions; Remove redundant or incorrect connections
/
6. Establish Code-Whiteboard Sync Mechanism: [Assumption: automation tools exist] Configure code change monitoring script; Set whiteboard auto-update rules (new file → new node, new import → new connection); Or manual maintenance: update corresponding whiteboard area after each code change
/
7. Use Whiteboard to Drive AI Programming (New Feature Development): Draw new module boxes and expected call relationships on whiteboard; Export whiteboard JSON and send to AI; Instruction: "Implement concrete code according to this architecture diagram"; AI generates files and function calls based on node names and connection directions
/
8. Use Whiteboard to Drive Code Refactoring (Architecture Adjustment): Delete/reconnect dependency lines between modules on whiteboard; Mark large modules to be split (e.g., payment_service split into payment_processor and payment_validator); Send modified whiteboard to AI: "Refactor code according to new architecture, list files to modify"
/
9. Use Whiteboard for Code Review: View whiteboard global architecture before review; Identify abnormal connections (e.g., frontend directly connecting to database, circular dependencies); Mark problem points on whiteboard; During discussion, point to whiteboard: "This call chain shouldn't exist"
/
10. Use Whiteboard to Accelerate Team Collaboration: Newcomers first view whiteboard for 1 minute to understand the big picture; Draw change scope on whiteboard during requirement review; Project whiteboard during technical planning meetings instead of code; Convert whiteboard annotations to development tasks after meeting
/
11. Maintain Whiteboard-Code Consistency: Check if whiteboard needs updating before each PR/MR merge; Periodically run auto-validation script: compare whiteboard JSON with actual code dependencies; When inconsistencies found, prioritize fixing whiteboard (because whiteboard is source of truth)
/
12. Extended Use Cases: Auto-generate whiteboard when taking over legacy projects for quick understanding; Mark hot paths on whiteboard during performance optimization; Check sensitive data flow on whiteboard during security audits; Draw service call topology on whiteboard during API design
/
13. [Gap Clarification] Specify your project type to optimize workflow: A) Monolith (single process, multiple modules) B) Microservices architecture (multiple services, RPC communication) C) Frontend-backend separation (frontend framework + backend API)? Default assumption A to continue
/
14. [Gap Clarification] Choose whiteboard granularity level: A) File level (each code file as one node) B) Class/function level (each class as one node) C) Service level (only show large modules)? Recommended: A for beginners, C for complex projects
/
15. Continuously Iterate Workflow: Weekly review if whiteboard reflects real architecture; Collect team feedback to optimize node naming and layout rules; Explore whiteboard integration with CI/CD (e.g., PR triggers whiteboard diff check); Share best practice cases to team knowledge base
