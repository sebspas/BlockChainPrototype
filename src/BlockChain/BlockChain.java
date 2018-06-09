package BlockChain;

import com.google.gson.GsonBuilder;
import com.sun.org.apache.xpath.internal.operations.Bool;

import java.util.ArrayList;

public class BlockChain {
    private ArrayList<Block> blockChain;

    private final static BlockChain instance = new BlockChain();
    public static BlockChain getInstance() { return instance; }
    private BlockChain() {
        blockChain = new ArrayList<>();
    }

    public void addBlock(Block b) {
        blockChain.add(b);
    }

    public Block getLastBlock() {
        return blockChain.get(blockChain.size()-1);
    }

    public String getJSON() {
        return new GsonBuilder().setPrettyPrinting().create().toJson(blockChain);
    }

    public Boolean isChainValid() {
        Block currentBlock;
        Block previousBlock;

        for (int i = 1; i < blockChain.size(); i++) {
            currentBlock = blockChain.get(i);
            previousBlock = blockChain.get(i - 1);

            if (!currentBlock.hash.equals(currentBlock.calculateHash())) {
                System.out.println("Current hashes not equal");
                return false;
            }

            if (!previousBlock.hash.equals(currentBlock.previousHash)) {
                System.out.println("Previous Hashes not equal");
                return false;
            }
        }

        return true;
    }
}
