Feature: self-service user registration
    Users want to be able to register themselves

    Background: registration form is open
        Given user navigated to /register/

    Scenario: user already exists
        Given user "jdoe" exists
        When fill registration form for user "jdoe"
        Then registration fails with error "Username already registered"

    Scenario: user use to short password
        When fill to short password "sad" in registration form for user "jdoe"
        Then it fails with error "Field must be between 6 and 40 characters long"