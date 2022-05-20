import PCASingle from "./components/PCASingle";
import PCADouble from "./components/PCADouble";
import Boxplot from "./components/Boxplot";
import LogFoldChange from "./components/LogFoldChange";
import PairwiseMachineLearning from "./components/PairwiseMachineLearning";
import SamplePvaluePCACombined from "./components/SamplePvaluePCACombined";
import SamplePvaluePCASingle from "./components/SamplePvaluePCASingle";
import PairwiseMachineLearningMatrix from "./components/PairwiseMachineLearingMatrix";
import LogFoldChangeMatrix from "./components/LogFoldChangeMatrix";
import PCADoubleMatrix from "./components/PCADoubleMatrix";
import PairwiseMultiPlot from "./components/PairwiseMultiPlot";
import AUC_PCA from "./components/AUC_PCA";

class Route {
    constructor(path, element, description){
        this.path = path;
        this.element = element;
        this.description = description
    }
}
const routing = [
    new Route("/PCA/Single", PCASingle, "PCA Single Dataset"),
    new Route("/PCA/Double/Pair", PCADouble, "PCA Two Datasets (Pair)"),
    new Route("/PCA/Double/Matrix", PCADoubleMatrix, "PCA Two Datasets (Matrix)"),
    new Route("/Boxplot", Boxplot, "Boxplot"),
    new Route("/LogFoldChange/Pair", LogFoldChange, "Log Fold Change correlation (Pair)"),
    new Route("/LogFoldChange/Matrix", LogFoldChangeMatrix, "Log Fold Change correlation (Matrix)"),
    new Route("/PairwiseMachineLearning/Pair", PairwiseMachineLearning, "Pairwise machine learning (Pair)"),
    new Route("/PairwiseMachineLearning/Matrix", PairwiseMachineLearningMatrix, "Pairwise machine learning (Matrix)"),
    new Route("/SamplePvaluePCA/Single", SamplePvaluePCASingle, "Sample p-value PCA (single)"),
    new Route("/SamplePvaluePCA/Combined", SamplePvaluePCACombined, "Sample p-value PCA (combined)"),
    new Route("/AUC_PCA", AUC_PCA, "AUC PCA"),
    new Route("/PairwiseMultiPlot", PairwiseMultiPlot, "Pairwise Multi Plot")];
export default routing;