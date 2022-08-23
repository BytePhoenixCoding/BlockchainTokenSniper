//SPDX-License-Identifier: UNLICENSED

/*

BlockchainTokenSniper: Honeypot checker smart contract

NOTE:

This contract is currently configured to work on BSC mainnet and PancakeSwap.

Want to change to use for a different blockchain / DEX? (Uniswap V2 fork)

- Replace exchangeRouterAddress with your custom DEX router address
- You may need to change swapExactETHForTokensSupportingFeeOnTransferTokens to whatever function name the DEX uses (ie. BakerySwap) etc
- Enable optimization and deploy on whatever blockchain you like with remix.ethereum.org

*/

pragma solidity ^0.8;

interface IERC20 {
    function balanceOf(address account) external view returns (uint);
    function approve(address spender, uint amount) external returns (bool);
}

interface IUniswapV2Router01 {
    function factory() external pure returns (address);
    function WETH() external pure returns (address);
    function getAmountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts);
}

interface IUniswapV2Router02 is IUniswapV2Router01 {
    function swapExactETHForTokensSupportingFeeOnTransferTokens(uint amountOutMin, address[] calldata path, address to, uint deadline) external payable;
    function swapExactTokensForTokensSupportingFeeOnTransferTokens(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline) external;
}

interface IWETH {
    function deposit() external payable;
}

contract HoneypotChecker {

    address public exchangeRouterAddress = 0x10ED43C718714eb63d5aA57B78B54704E256024E; //change this is needed
    IUniswapV2Router02 exchangeRouter = IUniswapV2Router02(exchangeRouterAddress);

    function buy(address baseToken, address token) public payable returns (uint, uint, uint, uint, uint, uint) {
        uint[] memory gas = new uint[](2);

        IERC20 _token = IERC20(token);
        IERC20 _baseToken = IERC20(baseToken);
        address[] memory path = new address[](2);

        if(baseToken != exchangeRouter.WETH()) {
            path[0] = exchangeRouter.WETH();
            path[1] = baseToken;
            exchangeRouter.swapExactETHForTokensSupportingFeeOnTransferTokens{value: msg.value}(0, path, address(this), block.timestamp + 20);
        }

        else {
            IWETH(baseToken).deposit{value: msg.value}();
        }

        uint amount = _baseToken.balanceOf(address(this));
        
        path = new address[](2);
        path[0] = baseToken;
        path[1] = token;

        uint expectedToken = exchangeRouter.getAmountsOut(amount, path)[1];
        _baseToken.approve(exchangeRouterAddress, type(uint).max);
        uint startGas = gasleft();
        exchangeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(amount, 0, path, address(this), block.timestamp + 20);
        gas[0] = startGas - gasleft();
        uint receivedToken = _token.balanceOf(address(this));

        path = new address[](2);
        path[0] = token;
        path[1] = baseToken;

        uint expectedBaseToken = exchangeRouter.getAmountsOut(receivedToken, path)[1];
        _token.approve(exchangeRouterAddress, type(uint).max);
        startGas = gasleft();
        exchangeRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(receivedToken, 0, path, address(this), block.timestamp + 20);
        gas[1] = startGas - gasleft();
        
        uint receivedBaseToken = _baseToken.balanceOf(address(this));

        return (expectedToken, receivedToken, gas[0], expectedBaseToken, receivedBaseToken, gas[1]);
    }

    receive() external payable {}
}