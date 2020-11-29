Feature: Edit user profile
As a SupplyHero user
I want to edit my user profile
So that my account can be accessed with new credentials

  Scenario: Edit email address (Normal Flow)
    Given user is logged on with an active account
    When user edits their email address
    Then the email address is updated on the user's profile

  Scenario: Edit password (Alternate Flow)
    Given user is logged on with an active account
    When user edits their password
    Then the password is updated on the user's profile

  Scenario: Edit email address with an already used email (Error Flow)
    Given user is logged on with an active account
    When user attempts to edit their email address with an existing one
    Then a "Email is already used." message is returned

  Scenario: Edit user profile without any new information (Error Flow)
    Given user is logged on with an active account
    When user attempts to edit user profile without providing new information
    Then a "An email or password is needed." message is returned

  Scenario: Edit email address with an invalid one (Error Flow)
    Given user is logged on with an active account
    When user attempts to edit their email address with an invalid one
    Then a "value is not a valid email address" message is sent