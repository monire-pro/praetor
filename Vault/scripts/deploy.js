import hre from "hardhat";

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("👮 Deploying contracts with account:", deployer.address);

  // 1. Deploy the Token
  const MNEE = await hre.ethers.getContractFactory("MockMNEE");
  const token = await MNEE.deploy();
  await token.waitForDeployment();
  const tokenAddress = await token.getAddress();
  console.log(`✅ Token Deployed at: ${tokenAddress}`);

  // 2. Deploy the Treasury
  const Treasury = await hre.ethers.getContractFactory("PraetorTreasury");
  const treasury = await Treasury.deploy(); // Deployer is automatically the owner
  await treasury.waitForDeployment();
  const treasuryAddress = await treasury.getAddress();
  console.log(`🏦 Treasury Deployed at: ${treasuryAddress}`);

  // 3. Fund the Treasury (So the AI has money to spend)
  console.log("💸 Funding Treasury...");
  const amount = hre.ethers.parseEther("5000"); // 5000 MNEE
  await token.transfer(treasuryAddress, amount);
  console.log("🎉 Treasury Funded with 5000 MNEE");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});