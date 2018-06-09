package Test;

import BlockChain.Block;
import BlockChain.BlockChain;

public class BlockChainMain {

    public static void main(String[] args) {
        BlockChain blockChain = BlockChain.getInstance();

        blockChain.addBlock(new Block("Origin block", "0"));
        blockChain.addBlock(new Block("Second block", blockChain.getLastBlock().hash));
        blockChain.addBlock(new Block("Third block", blockChain.getLastBlock().hash));

        System.out.println(blockChain.getJSON());
    }
}
