Feature: Log Out
As a SupplyHero user
I want to log out of the SupplyHero applicaiton
So that I can prevent other people from using my account

  Scenario: Logging Out (Normal Flow)
    Given user is logged on
     When user requests to log out
     Then user is logged out
     

  Scenario: Logging Out without being Logged In (Error Flow)
    Given user is not logged on
     When user requests to log out
     Then user is prompted "You are not logged in!" message