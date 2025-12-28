import hre from "hardhat";

async function main() {
  // 1. Get the Contract Address (Make sure this matches your .env!)
  const tokenAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; 
  
  // 2. Connect to the Contract
  // Note: We use hre.ethers directly
 const mnee = await hre.ethers.getContractAt("MockMNEE", tokenAddress);
  
  // 3. Check Balances
  const [deployer] = await hre.ethers.getSigners();
  const deployerBal = await mnee.balanceOf(deployer.address);
  const contractBal = await mnee.balanceOf(tokenAddress);

  console.log(`👤 User Balance:     ${hre.ethers.formatEther(deployerBal)} MNEE`);
  console.log(`🏦 Contract Balance: ${hre.ethers.formatEther(contractBal)} MNEE`);

  // 4. Deposit Funds into the Contract
  console.log("\n🔄 Depositing 50,000 MNEE into the Treasury...");
  
  // We parse the string "50000" into 18-decimal format
  const amount = hre.ethers.parseEther("50000");
  
  const tx = await mnee.transfer(tokenAddress, amount);
  await tx.wait();

  // 5. Verify New Balance
  const newBal = await mnee.balanceOf(tokenAddress);
  console.log(`✅ Success! Treasury Now Has: ${hre.ethers.formatEther(newBal)} MNEE`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});