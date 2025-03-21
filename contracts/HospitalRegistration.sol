// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract HospitalRegistration {
    struct Hospital {
        string name;
        address walletAddress;
    }

    Hospital[] public hospitals;

    function registerHospital(string memory name, address walletAddress) public {
        hospitals.push(Hospital(name, walletAddress));
    }

    function getHospitalCount() public view returns (uint) {
        return hospitals.length;
    }
}