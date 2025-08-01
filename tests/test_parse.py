import pytest
from xml.etree import ElementTree as ET
from unittest.mock import patch, Mock
from pubmed_scout.parse import (
    is_company_affiliation, 
    parse_fetch_response,
    EMAIL_PATTERN
)


class TestIsCompanyAffiliation:
    """Test cases for is_company_affiliation function."""
    
    def test_company_keywords_detected(self):
        """Test detection of company affiliations."""
        test_cases = [
            "BioTech Corp Research Division",
            "Pharma Inc. Drug Development",
            "Therapeutics LLC Innovation Lab",
            "Medical Corp GmbH"
        ]
        
        for affiliation in test_cases:
            assert is_company_affiliation(affiliation) is True
    
    def test_non_company_affiliations(self):
        """Test non-company affiliations are not detected."""
        test_cases = [
            "University of California, San Francisco",
            "Harvard Medical School",
            "Mayo Clinic Research Institute"
        ]
        
        for affiliation in test_cases:
            assert is_company_affiliation(affiliation) is False
    
    def test_case_insensitive_detection(self):
        """Test case-insensitive keyword detection."""
        assert is_company_affiliation("BIOTECH CORP") is True
        assert is_company_affiliation("pharma inc") is True


class TestEmailPattern:
    """Test cases for email regex pattern."""
    
    def test_valid_emails_matched(self):
        """Test valid email patterns are matched."""
        valid_emails = [
            "test@example.com",
            "researcher.name@biotech.co.uk",
            "contact+info@pharma-corp.org"
        ]
        
        for email in valid_emails:
            match = EMAIL_PATTERN.search(email)
            assert match is not None
            assert match.group() == email
    
    def test_invalid_emails_not_matched(self):
        """Test invalid email patterns are not matched."""
        invalid_emails = [
            "not-an-email",
            "@missing-local.com",
            "missing-domain@.com"
        ]
        
        for email in invalid_emails:
            match = EMAIL_PATTERN.search(email)
            assert match is None


class TestParseFetchResponse:
    """Test cases for parse_fetch_response function."""
    
    def test_parse_valid_xml(self):
        """Test parsing valid XML response."""
        xml_content = """
        <PubmedArticleSet>
            <PubmedArticle>
                <MedlineCitation Status="Publisher" Owner="NLM">
                <PMID Version="1">12345</PMID>
                <DateRevised>
                    <Year>2025</Year>
                    <Month>07</Month>
                    <Day>31</Day>
                </DateRevised>
                <Article PubModel="Print">
                    <Journal>
                    <ISSN IssnType="Print">1234-5678</ISSN>
                    <JournalIssue CitedMedium="Print">
                        <Volume>10</Volume>
                        <Issue>3</Issue>
                        <PubDate>
                        <Year>2025</Year>
                        <Month>Jul</Month>
                        <Day>30</Day>
                        </PubDate>
                    </JournalIssue>
                    <Title>Journal of Sample Research</Title>
                    <ISOAbbreviation>J Sample Res</ISOAbbreviation>
                    </Journal>
                    <ArticleTitle>Sample Study on BioTech Innovations</ArticleTitle>
                    <Abstract>
                    <AbstractText Label="BACKGROUND" NlmCategory="BACKGROUND">
                        This is a sample abstract for demonstrating PubMed EFetch XML output.
                    </AbstractText>
                    </Abstract>
                    <AuthorList CompleteYN="Y">
                    <Author ValidYN="Y">
                        <LastName>Doe</LastName>
                        <ForeName>John</ForeName>
                        <Initials>J</Initials>
                        <AffiliationInfo>
                        <Affiliation>BioTech Corp, San Francisco, CA, USA. john@biotech.com.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    </AuthorList>
                    <Language>eng</Language>
                    <PublicationTypeList>
                    <PublicationType UI="D016428">Journal Article</PublicationType>
                    </PublicationTypeList>
                </Article>
                <MedlineJournalInfo>
                    <Country>United States</Country>
                    <MedlineTA>J Sample Res</MedlineTA>
                    <NlmUniqueID>1234567</NlmUniqueID>
                    <ISSNLinking>1234-5678</ISSNLinking>
                </MedlineJournalInfo>
                </MedlineCitation>
                <PubmedData>
                <History>
                    <PubMedPubDate PubStatus="received">
                    <Year>2025</Year>
                    <Month>05</Month>
                    <Day>01</Day>
                    </PubMedPubDate>
                    <PubMedPubDate PubStatus="accepted">
                    <Year>2025</Year>
                    <Month>07</Month>
                    <Day>15</Day>
                    </PubMedPubDate>
                    <PubMedPubDate PubStatus="entrez">
                    <Year>2025</Year>
                    <Month>07</Month>
                    <Day>31</Day>
                    </PubMedPubDate>
                </History>
                <PublicationStatus>ppublish</PublicationStatus>
                <ArticleIdList>
                    <ArticleId IdType="pubmed">12345</ArticleId>
                    <ArticleId IdType="doi">10.1234/sample.2025.00123</ArticleId>
                </ArticleIdList>
                </PubmedData>
            </PubmedArticle>
        </PubmedArticleSet>
        """
        
        root = ET.fromstring(xml_content)
        articles = parse_fetch_response(root)
        
        assert len(articles) == 1
        article = articles[0]
        assert article["PubmedID"] == "12345"
        assert article["Title"] == "Sample Study on BioTech Innovations"
        assert article["Publication Date"] == " 2025 Jul 30"
        assert "John Doe" in article["Non-Academic Authors"]
        assert "BioTech Corp" in article["Company Affiliations"]
    
    @patch('pubmed_scout.parse.typer.Exit')
    def test_parse_none_root(self, mock_exit):
        """Test parsing with None root element."""
        parse_fetch_response(None)
        mock_exit.assert_called_once_with(1)
    
    def test_parse_empty_xml(self):
        """Test parsing empty XML."""
        xml_content = "<PubmedArticleSet></PubmedArticleSet>"
        root = ET.fromstring(xml_content)
        
        articles = parse_fetch_response(root)
        
        assert articles == []