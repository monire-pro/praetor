import "@nomicfoundation/hardhat-toolbox";
import dotenv from "dotenv";

dotenv.config();

/** @type {import("hardhat/config").HardhatUserConfig} */
const config = {
  solidity: "0.8.19",
  networks: {
    // Local development network
    hardhat: {},

    // MNEE Testnet (update RPC URL when finalized)
    mnee_testnet: {
      url: process.env.RPC_URL || "https://rpc-endpoint-here",
      accounts: process.env.PRIVATE_KEY
        ? [process.env.PRIVATE_KEY]
        : []
    }
  }
};

export default config;
