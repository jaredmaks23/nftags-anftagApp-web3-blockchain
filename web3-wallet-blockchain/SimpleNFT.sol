// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleNFT {
    mapping(address => uint256) public balances;
    mapping(uint256 => string) public nftInfo;

    function mint(address to, uint256 nftId, string memory info) public {
        balances[to]++;
        nftInfo[nftId] = info;
    }

    function balanceOf(address owner) public view returns (uint256) {
        return balances[owner];
    }

    function updateNFTInfo(uint256 nftId, string memory newInfo) public {
        nftInfo[nftId] = newInfo;
    }
}
