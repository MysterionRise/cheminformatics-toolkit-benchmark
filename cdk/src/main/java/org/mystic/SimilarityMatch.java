package org.mystic;

import org.openscience.cdk.exception.CDKException;
import org.openscience.cdk.fingerprint.HybridizationFingerprinter;
import org.openscience.cdk.interfaces.IAtomContainer;
import org.openscience.cdk.silent.SilentChemObjectBuilder;
import org.openscience.cdk.similarity.Tanimoto;
import org.openscience.cdk.smiles.SmilesParser;

import java.util.BitSet;

public class SimilarityMatch {
    public static void main(String[] args) throws CDKException {
        SmilesParser smilesParser = new SmilesParser(
                SilentChemObjectBuilder.getInstance()
        );
        String smiles1 = "CC(C)C=CCCCCC(=O)NCc1ccc(c(c1)OC)O";
        String smiles2 = "COC1=C(C=CC(=C1)C=O)O";
        IAtomContainer mol1 = smilesParser.parseSmiles(smiles1);
        IAtomContainer mol2 = smilesParser.parseSmiles(smiles2);
        HybridizationFingerprinter fingerprinter = new HybridizationFingerprinter();
        BitSet bitset1 = fingerprinter.getFingerprint(mol1);
        BitSet bitset2 = fingerprinter.getFingerprint(mol2);
        float tanimoto = Tanimoto.calculate(bitset1, bitset2);
        System.out.println(tanimoto);
    }
}
