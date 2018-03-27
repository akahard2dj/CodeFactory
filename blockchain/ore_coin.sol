pragma solidity ^0.4.21;

contract OreOreCoin {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    
    function OreOreCoin(uint256 _supply, string _name, string _symbol, uint8 _decimals) public {
        balanceOf[msg.sender] = _supply;
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _supply;
    }
    
    function transfer(address _to, uint256 _value) public {
        if (balanceOf[msg.sender] < _value) assert(false);
        if (balanceOf[_to] + _value < balanceOf[_to]) assert(false);
        
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        
        Transfer(msg.sender, _to, _value);
    }
}
