# MF-017: Report Renderer

## Priority
**SHOULD FINISH** - Makes project easier to demo

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- MF-014 (Board Backend) - needs report endpoint
- MF-015 (Board Frontend) - needs base UI structure

## Parallel Work
Can work in parallel with MF-016 (Mission Detail Panel) and MF-018 (Dependency Graph)

## Objective
Render the generated Markdown evidence report in the Mission Board with proper styling and formatting.

## Tasks
- [ ] Create report renderer component
- [ ] Integrate Markdown parser (react-markdown or similar)
- [ ] Style Markdown elements:
  - Headings (h1-h6)
  - Tables
  - Code blocks with syntax highlighting
  - Lists (ordered and unordered)
  - Blockquotes
  - Links
- [ ] Add copy-to-clipboard button for entire report
- [ ] Add download button (save as .md file)
- [ ] Show report generation status
- [ ] Show helpful message if report doesn't exist yet
- [ ] Add loading state while fetching report
- [ ] Handle large reports (pagination or scroll)

## Acceptance Criteria
- [ ] Markdown renders correctly with all elements styled
- [ ] Tables are readable and properly formatted
- [ ] Code blocks have syntax highlighting
- [ ] Copy button works reliably
- [ ] Download button saves correct .md file
- [ ] Report is readable and professional-looking
- [ ] Works with reports of various sizes
- [ ] Loading and error states are clear
- [ ] Report updates when regenerated

## Technical Notes
- Use react-markdown for parsing
- Use react-syntax-highlighter for code blocks
- Consider remark-gfm for GitHub Flavored Markdown (tables)
- Style with Tailwind CSS for consistency
- Add print styles for PDF export (stretch goal)
- Lazy load for large reports

## Estimated Effort
**2-3 hours** (hackathon pace)

## Developer Assignment
Frontend Developer (can work in parallel with MF-016)
