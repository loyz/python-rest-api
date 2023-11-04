# Outline of Coding Challenge
from 
https://raw.githubusercontent.com/SUMM-AI-Github/202309-backend-coding-challenge/main/README.md

## 🎯 Goal

Your mission, should you choose to accept it, is to create a Django API capable of translating text provided in HTML or plain text format. Your API should serve as a bridge between users and a third-party translation service.

## 🔑 Requirements

To successfully complete this challenge, make sure your Django API adheres to the following requirements:

- **Text Translation**: Your API should receive input text, translate it using a third-party API, and return the translated text to the user.

- **Content Type Specification**: Implement an attribute in your API where users can specify the content type of the input text (e.g., HTML, plain text, etc.). You can name this attribute as you prefer.

- **HTML Handling**: When the input text is in HTML format, preserve all outer tags (such as h1, h2, p, etc.), while translating only the inner text portions. This ensures that the document structure remains intact.

- **User Associations**: Attach translations to specific users so that each user's translations can be tracked and retrieved.

- **Translation Retrieval**: Provide a feature in your API to fetch all translations associated with a particular user.

### 📜 Example: Translating Inner Parts

Let's illustrate the HTML handling and translation process with an example input:

```html
"<h2 class='editor-heading-h2' dir='ltr'><span>hallo1 as headline</span></h2><p class='editor-paragraph' dir='ltr'><br></p><p class='editor-paragraph' dir='ltr'><span>hallo2 as paragraph</span></p><p class='editor-paragraph' dir='ltr'><span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span></p>"
```

In this case, your API should extract the following three text portions for translation:

1. `<span>hallo1 as headline</span>`
2. `<span>hallo2 as paragraph</span>`
3. `<span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span>`

After translation, these segments should be reassembled into the original HTML structure, preserving the tags.

# Strategy

1. Setup Django, PostgreSQL and Django REST API Framework in Docker
2. Custom User Model: 
    - User-Authentication with email / Permissions for staff / Future Proof
        Fields:
        - email (EmailField)
        - name (CharField)
        - is_active (BooleanField)
        - is_staff (BooleanField)
    - User model manager
        - Hash password
        - Create superuser
    - Create Custom Manager for CLI
3. App for translating User Input
    a) Filter HTML
        - get all valid HTML Tags from W3C? or
        - check with RegEx https://www.geeksforgeeks.org/how-to-validate-html-tag-using-regular-expression/ or
        - check with node https://www.tutorialspoint.com/how-to-check-if-a-string-is-html-or-not-using-javascript#:~:text=Use%20the%20nodeType%20property%20of,the%20type%20of%20HTML%20element.
    b) Translate String
    c) Reapply HTML-Tags
    d) Send Answer
        - reassembled HTML
        - info about invalid HTML
    d) create report and save meta-data to db: 
        - user request
        - answer
        - statistics
    
