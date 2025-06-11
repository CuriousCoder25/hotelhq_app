# Document Verification Testing Guide

## Prerequisites
1. Ensure MySQL is running with the hotel_management database
2. Verify that the customer table has the required columns for document verification
3. Have test customer accounts with uploaded documents

## Testing Steps

### 1. Start the Application
```cmd
cd c:\Users\gaura\Desktop\hotelhq_app
start_hotel_app.bat
```
Or manually:
```cmd
cd c:\Users\gaura\Desktop\hotelhq_app
myenv\Scripts\activate
python app.py
```

### 2. Create Test Data

#### A. Create Test Customers (via Staff Dashboard)
1. Login as admin/staff
2. Go to Staff Dashboard
3. Click "Add New Customer"
4. Create test customers with valid details

#### B. Upload Test Documents (Customer Portal)
1. Login as a customer
2. Go to Customer Portal
3. Upload ID document and address proof
4. Logout and login as staff

### 3. Test Document Verification Workflow

#### A. View Document Queue
1. Access Staff Dashboard (`/staff_dashboard`)
2. Check "Document Verification Queue" section
3. Verify that pending customers appear in the list
4. Check that the queue count is accurate

#### B. Test "View Docs" Function
1. Click "View Docs" for any customer
2. Verify modal opens with customer information
3. Check that uploaded documents are displayed
4. Test image click-to-zoom (opens in new tab)
5. Test download functionality
6. Verify customer information section shows correctly

#### C. Test Document Approval
1. Click "Approve" button (either in queue or modal)
2. Verify confirmation dialog appears
3. Enter optional approval notes
4. Check for loading state (spinner)
5. Verify success message appears
6. Confirm page reloads and status updates
7. Check database to verify record update

#### D. Test Document Rejection
1. Click "Reject" button
2. Verify confirmation dialog appears
3. Try submitting without notes (should require notes)
4. Enter rejection reason
5. Check loading state and success message
6. Verify status update in queue and database

#### E. Test Reset to Pending
1. Click "Reset to Pending" button
2. Verify confirmation dialog
3. Enter optional notes
4. Check that status resets properly
5. Verify customer reappears in pending queue

### 4. Test Error Scenarios

#### A. Network Errors
1. Disconnect internet briefly
2. Try verification actions
3. Verify proper error messages appear
4. Check that buttons are re-enabled after error

#### B. Invalid Customer ID
1. Manually test API with invalid customer ID
2. Verify proper 404 error response

#### C. Missing Documents
1. Test with customer who hasn't uploaded documents
2. Verify appropriate "no documents" message
3. Check that verification actions still work

### 5. Test Database Integration

#### A. Verify Column Updates
```sql
SELECT User_ID, document_status, verification_notes, verified_by, verification_date 
FROM customer 
WHERE document_status IS NOT NULL;
```

#### B. Check Timestamp Accuracy
- Verify verification_date matches when action was performed
- Check that verified_by contains correct staff username

### 6. Test UI/UX Improvements

#### A. Visual Elements
- Check status badge colors (green=approved, red=rejected, yellow=pending)
- Verify loading spinners appear during operations
- Test responsive design on different screen sizes

#### B. User Feedback
- Confirm all actions provide clear success/error messages
- Test that confirmation dialogs are informative
- Verify tooltips appear on action buttons

### 7. Performance Testing

#### A. Large Document Queue
1. Create multiple test customers with pending documents
2. Verify queue loads quickly
3. Test scrolling in queue table
4. Check that actions remain responsive

#### B. Document Loading
1. Test with various document sizes/formats
2. Verify images load properly in modal
3. Check download speeds for large files

## Expected Results

### Successful Operation Indicators:
- ✅ Document queue shows accurate pending count
- ✅ "View Docs" modal displays documents clearly
- ✅ All verification actions provide proper feedback
- ✅ Database updates reflect verification changes
- ✅ Status badges show correct colors
- ✅ Loading states work properly
- ✅ Error handling is graceful

### Common Issues and Solutions:

#### Issue: Documents not showing in modal
**Solution**: Check that documents are in `static/documents/customers/` directory with correct naming pattern

#### Issue: Verification buttons not working
**Solution**: Verify staff authentication and check browser console for JavaScript errors

#### Issue: Database errors during verification
**Solution**: Ensure customer table has required columns and database connection is stable

#### Issue: Images not loading
**Solution**: Check file permissions on static directory and verify file paths

## Security Verification

1. **Authentication**: Verify only staff can access verification endpoints
2. **Authorization**: Check that customers cannot verify their own documents
3. **Input Validation**: Confirm API validates all inputs properly
4. **File Access**: Ensure document files are only accessible to authorized users

## Conclusion

After completing all tests, the document verification system should provide:
- Smooth workflow for staff to review and verify customer documents
- Clear visual feedback for all operations
- Proper error handling and recovery
- Accurate database updates and audit trail
- Enhanced user experience with modern UI elements
