#include "maxcut.h"
#include "nlopt.h"
#include "Exceptions.h"

using namespace qtorch;

int main( int argc, char *argv[]){
    /*
     * Read in pertinent data
     */
    std::string graphFilePath(argv[1]);
    int pVal = 1;
    int procSec = atoi(argv[2]);
    std::string outFilePath(argv[3]);
    std::vector<double> gammasAndBetas;
    mkdir("tmp", 0777);

    /*
     * Use dummy angles, doesn't matter for what we're doing
     */
    for( int i = 0 ; i < 2 * pVal ; i++ ){
        double z = 1;
        gammasAndBetas.push_back(z);
    }

    ExtraData e(pVal, graphFilePath.c_str());
    std::ofstream maxCutCircuitQasm("tmp/tempMaxCut.qasm");
    maxCutCircuitQasm << e.numQubits << std::endl;
    outputInitialPlusStateToFile(maxCutCircuitQasm, e.numQubits);
    applyU_CsThenU_Bs(e.pairs, pVal, gammasAndBetas, e.numQubits, maxCutCircuitQasm);
    maxCutCircuitQasm.close();
    std::vector<std::pair<int, int>> optContract;
    preProcess("tmp/tempMaxCut.qasm", optContract, procSec);
    std::ofstream optContractOutput(outFilePath);
    for( const auto& p : optContract){
        optContractOutput << p.first << " " << p.second << std::endl;
    }
}
