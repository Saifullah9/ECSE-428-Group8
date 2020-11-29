Feature: Delete School Supply List
As a SupplyHero user
I want to be able to delete a school supply list
So that I can remove it from my account


    Scenario: Delete School Supply List (Normal Flow)
    Given user has an account with at least one supply list
     When user requests to delete this school supply list
     Then the school supply list no longer exists for this user

    Scenario: Delete School Supply List with no Existing School Supply List (Error Flow)
    Given user who already have an existing account with no supply lists
     When user requests to delete this school supply list
     Then user is shown "You have no school supply lists." message




