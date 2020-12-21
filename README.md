# BulkCertGenerator_MC_Public
Bulk Certificate Generator with MailChimp Integration (Python)

A simple two-part Python script used for the FUTURE Conference 2020: 

##CertGenerator: 
- Consumes a CSV file of names and a PNG template, email addresses etc. 
- Creates a local dir of PNG and PDF certificates for each CSV entry 
- (Pandas, OpenCV and PIL).

##MCScript03: 
- Consumes account info (API Key, etc) of a given MailChimp account.
- Uploads the PDF certificates onto the MailChimp file system;
- Automatically generates URLs corresponding to each PDF;
- Automatically matched and assigns URLs to existing contacts in MailChimp account.
- Automatically adds hasCertificate tag (flag) to contacts.
- (MailChimp3 API)