# Testing Checklist - Chat Feature

## Pre-Flight Checks

- [ ] Container is running (`bash run_container.sh`)
- [ ] Can access http://localhost:7860
- [ ] LM Studio is running with a model loaded (or OpenAI key is set)
- [ ] "Chat with LLM" tab is visible in Gradio

## Basic Chat Tests

### Test 1: Simple Query
**Action:** Click on "Chat with LLM" tab, type: "Hello"
- [ ] Message appears in chat history
- [ ] LLM responds
- [ ] No error messages

### Test 2: Query Library Status
**Action:** Type: "How many books are in the library?"
- [ ] LLM responds with a count
- [ ] Response is meaningful

### Test 3: List All Books
**Action:** Type: "Show me all books"
- [ ] Gets list of books (should show sample books)
- [ ] Shows book IDs, titles, authors, ISBNs

### Test 4: Add a Book
**Action:** Type: "Add a new book called 'The Hobbit' by J.R.R. Tolkien with ISBN 978-0547928227"
- [ ] LLM adds the book
- [ ] Responds with success message
- [ ] Includes book ID in response

### Test 5: List Patrons
**Action:** Type: "Show me all patrons"
- [ ] Gets list of patrons
- [ ] Shows patron details

### Test 6: Register a Patron
**Action:** Type: "Register a new patron named Alice Smith with email alice@example.com and phone 555-1234"
- [ ] LLM registers the patron
- [ ] Responds with success and patron ID

### Test 7: Borrow a Book
**Action:** Type: "Borrow book 1 for patron 1" or "Let patron 1 borrow book 1"
- [ ] LLM executes the borrow operation
- [ ] Returns due date

### Test 8: Check Overdue Books
**Action:** Type: "Are there any overdue books?"
- [ ] LLM checks for overdue items
- [ ] Responds with list (initially should be "No overdue books")

### Test 9: Multi-Step Operation
**Action:** Type: "Register patron Jane Doe (jane@email.com, 555-5678) then show me all patrons"
- [ ] LLM registers Jane
- [ ] Shows updated patron list
- [ ] Jane appears in the list

### Test 10: Complex Task
**Action:** Type: "Register John Brown (john.brown@email.com, 555-1111), register Sarah Lee (sarah.lee@email.com, 555-2222), and lend them both book 2 for 21 days"
- [ ] LLM performs all operations
- [ ] All succeed with no errors
- [ ] Shows confirmation for each action

## Error Handling Tests

### Test 11: Invalid Book ID
**Action:** Type: "Get info about book 999"
- [ ] LLM responds with "not found" message
- [ ] No crash, graceful error

### Test 12: Invalid Patron ID
**Action:** Type: "Get info about patron 999"
- [ ] LLM responds with "not found" message
- [ ] No crash, graceful error

### Test 13: Borrow unavailable book
**Action:** (First borrow book 1 to patron 1, then try same)
**Action:** Type: "Borrow book 1 for patron 2"
- [ ] LLM handles it gracefully
- [ ] Returns error message about book not being available

### Test 14: Return non-borrowed book
**Action:** Type: "Return book 999"
- [ ] LLM responds with error
- [ ] No crash

## UI/UX Tests

### Test 15: Chat History
**Action:** Send several messages
- [ ] All appear in chat history
- [ ] User messages show on one side
- [ ] LLM responses on the other
- [ ] Proper formatting

### Test 16: Clear Input After Send
**Action:** Send a message
- [ ] Message input box is cleared
- [ ] Ready for next message

### Test 17: Multi-line Input
**Action:** Type message with multiple lines in input box
- [ ] All lines are sent
- [ ] LLM processes correctly

## Performance Tests

### Test 18: Response Time
**Action:** Send: "List all books"
- [ ] Response within 5-10 seconds (LM Studio)
- [ ] Response within 3-5 seconds (OpenAI)
- [ ] No timeout errors

### Test 19: Multiple Consecutive Messages
**Action:** Send 5 messages rapidly
- [ ] All are processed
- [ ] No errors from rapid requests

## Service-Specific Tests

### For LM Studio:
- [ ] Works with "Show me all books"
- [ ] Works with "Add a book called Test by Author, ISBN 123"
- [ ] No 400 Bad Request errors

### For OpenAI:
- [ ] Works with API key
- [ ] Uses function calling (if supported)
- [ ] Handles tool calls properly

## Documentation Tests

- [ ] README.md updated
- [ ] CHAT_GUIDE.md available and readable
- [ ] ERROR_FIX.md explains the issue
- [ ] QUICKSTART.md works

## Final Verification

- [ ] All chat tests passed
- [ ] No errors in terminal output
- [ ] Container running smoothly
- [ ] Ready for production use

---

## Test Results Summary

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Simple Query | ✓/✗ | |
| 2 | Query Library | ✓/✗ | |
| 3 | List Books | ✓/✗ | |
| 4 | Add Book | ✓/✗ | |
| 5 | List Patrons | ✓/✗ | |
| 6 | Register Patron | ✓/✗ | |
| 7 | Borrow Book | ✓/✗ | |
| 8 | Check Overdue | ✓/✗ | |
| 9 | Multi-Step | ✓/✗ | |
| 10 | Complex Task | ✓/✗ | |
| 11 | Invalid Book | ✓/✗ | |
| 12 | Invalid Patron | ✓/✗ | |
| 13 | Unavailable Book | ✓/✗ | |
| 14 | Return Non-borrowed | ✓/✗ | |
| 15 | Chat History | ✓/✗ | |
| 16 | Clear Input | ✓/✗ | |
| 17 | Multi-line Input | ✓/✗ | |
| 18 | Response Time | ✓/✗ | |
| 19 | Rapid Messages | ✓/✗ | |

---

## Known Issues & Workarounds

### LM Studio
- **Issue:** First message may take 5-10 seconds
  - **Workaround:** Wait for model to load in LM Studio first

- **Issue:** Model memory limits
  - **Workaround:** Use a smaller model or restart LM Studio

### OpenAI
- **Issue:** May have rate limits
  - **Workaround:** Wait a moment between rapid requests

---

## Support

If a test fails:
1. Check ERROR_FIX.md for 400 errors
2. Check QUICKSTART.md troubleshooting
3. Review CHAT_GUIDE.md for configuration
4. Check container logs: `docker logs librarian-librarian-1`
