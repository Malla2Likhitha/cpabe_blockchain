// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControl {
    address public owner;
    mapping(address => bool) public authorizedUsers;
    string private ipfsCID;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }

    // Grant access to a user (owner only)
    function grantAccess(address user) public onlyOwner {
        authorizedUsers[user] = true;
    }

    // Check if the caller has access
    function checkAccess() public view returns (bool) {
        return authorizedUsers[msg.sender];
    }

    // Set the IPFS CID (owner only)
    function setCID(string memory _cid) public onlyOwner {
        ipfsCID = _cid;
    }

    // Get the IPFS CID (anyone can call this)
    function getCID() public view returns (string memory) {
        return ipfsCID;
    }
}

