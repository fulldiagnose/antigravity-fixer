"""Supported countries and constants for Antigravity eligibility."""

# Countries where Antigravity free tier is available
# Source: https://developers.google.com/gemini-code-assist/resources/available-locations
SUPPORTED_COUNTRIES = {
    # Americas
    "American Samoa", "Anguilla", "Antigua and Barbuda", "Argentina", "Aruba",
    "Bahamas", "Barbados", "Belize", "Bermuda", "Bolivia", "Brazil",
    "British Virgin Islands", "Canada", "Caribbean Netherlands", "Cayman Islands",
    "Chile", "Colombia", "Costa Rica", "Curaçao", "Dominica",
    "Dominican Republic", "Ecuador", "El Salvador", "Falkland Islands",
    "French Guiana", "Grenada", "Guadeloupe", "Guatemala", "Guyana",
    "Haiti", "Honduras", "Jamaica", "Martinique", "Mexico", "Montserrat",
    "Nicaragua", "Panama", "Paraguay", "Peru", "Puerto Rico",
    "Saint Barthélemy", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Martin", "Saint Pierre and Miquelon", "Saint Vincent",
    "Sint Maarten", "South Georgia", "Suriname", "Trinidad and Tobago",
    "Turks and Caicos Islands", "United States", "Uruguay", "Venezuela",
    # Europe
    "Åland Islands", "Albania", "Andorra", "Armenia", "Austria", "Belgium",
    "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Faroe Islands", "Finland",
    "France", "Georgia", "Germany", "Gibraltar", "Greece", "Greenland",
    "Guernsey", "Holy See", "Hungary", "Iceland", "Ireland", "Isle of Man",
    "Italy", "Jersey", "Kosovo", "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro",
    "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal",
    "Romania", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain",
    "Svalbard and Jan Mayen", "Sweden", "Switzerland", "Ukraine",
    "United Kingdom",
    # Africa
    "Algeria", "Angola", "Ascension Island", "Benin", "Botswana",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
    "Central African Republic", "Chad", "Comoros", "Congo",
    "Côte d'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea",
    "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
    "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya",
    "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
    "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
    "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone",
    "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania",
    "Togo", "Tristan da Cunha", "Tunisia", "Uganda", "Zambia", "Zimbabwe",
    # Asia
    "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan",
    "British Indian Ocean Territory", "Brunei", "Cambodia", "China",
    "Christmas Island", "Cocos Islands", "Hong Kong", "India", "Indonesia",
    "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait",
    "Kyrgyzstan", "Laos", "Lebanon", "Macau", "Malaysia", "Maldives",
    "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan",
    "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
    "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan",
    "Thailand", "Timor-Leste", "Turkey", "Turkmenistan",
    "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen",
    # Oceania
    "Antarctica", "Australia", "Cook Islands", "Fiji",
    "French Polynesia", "Guam", "Kiribati", "Marshall Islands",
    "Micronesia", "Nauru", "New Caledonia", "New Zealand", "Niue",
    "Norfolk Island", "Northern Mariana Islands", "Palau",
    "Papua New Guinea", "Pitcairn Islands", "Samoa", "Solomon Islands",
    "Tokelau", "Tonga", "Tuvalu", "Vanuatu", "Wallis and Futuna",
}

# Antigravity OAuth endpoints
ANTIGRAVITY_OAUTH_URL = (
    "https://accounts.google.com/o/oauth2/auth"
    "?client_id=1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com"
    "&redirect_uri=https%3A%2F%2Fantigravity.google%2Foauth-callback"
    "&response_type=code"
    "&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform"
    "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email"
    "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile"
    "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcclog"
    "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fexperimentsandconfigs"
    "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faicode"
    "+openid"
    "&access_type=offline"
    "&prompt=consent"
    "&code_challenge_method=S256"
)

# Google account URLs
AGE_VERIFICATION_URL = "https://myaccount.google.com/age-verification"
COUNTRY_CHECK_URL = "https://policies.google.com/terms?hl=en"
CONNECTED_APPS_URL = "https://myaccount.google.com/connections"
PHONE_NUMBERS_URL = "https://myaccount.google.com/phone"
SUBSCRIPTION_URL = "https://one.google.com/"

# Windows paths
GEMINI_HOME = "~/.gemini"
GEMINI_CLI_CACHE = "~/.gemini/antigravity-cli"
GEMINI_IDE_STATE = "~/.gemini/antigravity"
CREDENTIAL_KEY = "gemini:antigravity"
