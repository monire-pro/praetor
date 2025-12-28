// contracts/scripts/deploy_treasury.js
import hardhat from "hardhat";
const { ethers, network } = hardhat; // Extract ethers from the default export

async function main() {
  const [deployer] = await ethers.getSigners();
  const networkName = network.name;

  console.log(`\n🚀 Deploying to network: ${networkName}`);
  console.log("👮 Deploying Account:", deployer.address);

  let mneeAddress;

  // 1. DETERMINE WHICH TOKEN TO USE
  if (networkName === "localhost" || networkName === "hardhat") {
    console.log("\n⚠️  Localhost detected! Deploying Fake MNEE Token...");
    
    const MockToken = await ethers.getContractFactory("MockMNEE");
    const mockToken = await MockToken.deploy();
    await mockToken.waitForDeployment();
    
    mneeAddress = await mockToken.getAddress();
    console.log("✅ Fake MNEE deployed to:", mneeAddress);
  } else {
    // REAL TESTNET: Use the official address
    mneeAddress = "0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF";
    console.log("\n🌍 Public Testnet detected! Using official MNEE:", mneeAddress);
  }

  // 2. DEPLOY THE TREASURY
  console.log("\n🏦 Deploying Praetor Treasury...");
  const Treasury = await ethers.getContractFactory("PraetorTreasury");
  
  const treasury = await Treasury.deploy(deployer.address, mneeAddress);
  await treasury.waitForDeployment();
  
  const treasuryAddress = await treasury.getAddress();

  console.log("----------------------------------------------------");
  console.log("🎉 SUCCESS! Treasury Deployed");
  console.log("📍 Treasury Address:", treasuryAddress);
  console.log("🔑 Linked Token:", mneeAddress);
  console.log("----------------------------------------------------");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});