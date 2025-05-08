// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControl {
    mapping(address => bool) public authorizedUsers;

    function grantAccess(address user) public {
        authorizedUsers[user] = true;
    }

    function checkAccess() public view returns (bool) {
        return authorizedUsers[msg.sender];
    }
}

