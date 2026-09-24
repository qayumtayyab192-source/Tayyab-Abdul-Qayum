#include <iostream>
#include <fstream>   
#include <sstream>   
#include <string>
#include <vector>
#include <cmath>
#include <filesystem>

namespace fs = std::filesystem;

std::vector<std::vector<double>> MatrixMultiplierWithBias(std::vector<std::vector<double>> MatrixA, std::vector<std::vector<double>> MatrixB, double Bias) {
    int RowsA = MatrixA.size();
    int ColumnsA = MatrixA[0].size();
    int RowsB = MatrixB.size();
    int ColumnsB = MatrixB[0].size();

    std::vector<std::vector<double>> ResultantMatrix(RowsA, std::vector<double>(ColumnsB, 0.0));

    for (int i = 0; i < RowsA; i++) {
        for (int j = 0; j < ColumnsB; j++) {
            for (int k = 0; k < ColumnsA; k++) {
                ResultantMatrix[i][j] += MatrixA[i][k] * MatrixB[k][j];
            }
            ResultantMatrix[i][j] += Bias;
        }
    }

    return ResultantMatrix;
}

std::vector<std::vector<double>> MatrixCreator(std::string FileName) {
    std::ifstream FilePath(FileName);

    std::string FileLine;
    std::vector<std::vector<double>> MatrixA;

    while (std::getline(FilePath, FileLine)) {
        if (FileLine.empty()) continue;
        std::vector<double> chem_row;
        std::stringstream chem_ss(FileLine);
        double chemterm;
        while (chem_ss >> chemterm) {
            chem_row.push_back(chemterm);
        }
        if (!chem_row.empty()) {
            MatrixA.push_back(chem_row);
        }
    }
    FilePath.close();

    return MatrixA;
}

void EditFile(std::string FileName, std::vector<std::vector<double>> MatrixWorkingWith) {
    std::ofstream ChangedWeights(FileName);
    int Repetitions = MatrixWorkingWith.size();

    if (ChangedWeights.is_open()) {
        for (int i = 0; i < Repetitions; i++) {
            ChangedWeights << MatrixWorkingWith[i][0] << "\n";
        }
        ChangedWeights.close();
    }
}

int main() {
    std::cout << "[1/6] Program started." << std::endl;

    fs::path base_dir = fs::current_path();

    fs::path matrices_path = base_dir / "Chemical_Properties" / "Chemical_Matrices.txt";
    fs::path predictions_path = base_dir / "Chemical_Properties" / "Predicted_Solubility.txt";
    fs::path weight_path = base_dir / "Chemical_Properties" / "Weights.txt";
    fs::path solublitiy_path = base_dir / "Chemical_Properties" / "Actual_Solubility.txt";
    fs::path bias_path = base_dir / "Chemical_Properties" / "Bias.txt";

    std::ifstream chemfile(matrices_path);
    std::ifstream weightFile(weight_path);
    std::ifstream biasFile(bias_path);
    std::ifstream solubilityFile(solublitiy_path);

    if (!chemfile || !weightFile || !biasFile || !solubilityFile) {
        std::cerr << "ERROR: Failed to open one or more input files!" << std::endl;
        return 1;
    }

    std::cout << "[2/6] Files opened successfully." << std::endl;

    std::vector<std::vector<double>> MatrixA = MatrixCreator(matrices_path.string());
    std::vector<std::vector<double>> MatrixB = MatrixCreator(weight_path.string());
    std::vector<std::vector<double>> VectorSolubility = MatrixCreator(solublitiy_path.string());

    double bias = 0.0;
    biasFile >> bias;
    biasFile.close();

    std::cout << "[3/6] Reading Chemical_Matrices.txt..." << std::endl;

    chemfile.close();
    std::cout << "      -> MatrixA loaded: " << MatrixA.size() << " rows." << std::endl;

    std::cout << "[4/6] Reading Weights.txt..." << std::endl;
    double weightVal;

    weightFile.close();
    std::cout << "      -> MatrixB loaded: " << MatrixB.size() << " elements." << std::endl;

    std::cout << "[5/6] Reading Actual_Solubility.txt..." << std::endl;
    
    solubilityFile.close();
    std::cout << "      -> VectorSolubility loaded: " << VectorSolubility.size() << " elements." << std::endl;

    if (MatrixA.empty() || MatrixB.empty() || VectorSolubility.empty()) {
        std::cerr << "ERROR: One or more data arrays are empty!" << std::endl;
        return 1;
    }

    int RowsA = MatrixA.size();
    int ColumnsA = MatrixA[0].size();
    int RowsB = MatrixB.size();
    int ColumnsB = MatrixB[0].size();

    std::cout << "      -> MatrixA dimensions: " << RowsA << " x " << ColumnsA << std::endl;

    if (ColumnsA != RowsB) {
        std::cerr << "CRITICAL ERROR: MatrixA columns (" << ColumnsA 
                  << ") do not match Weight count (" << RowsB << ")!" << std::endl;
        return 1;
    }

    if (RowsA != VectorSolubility.size()) {
        std::cerr << "CRITICAL ERROR: MatrixA rows (" << RowsA 
                  << ") do not match Target Solubility rows (" << VectorSolubility.size() << ")!" << std::endl;
        return 1;
    }

    std::cout << "[6/6] Starting Training Loop..." << std::endl;

    double MeanError = 0.0;
    int epoch = 0;
    int max_epochs = 100000;
    double learning_rate = 0.00001;

    std::vector<std::vector<double>> predictions = MatrixMultiplierWithBias(MatrixA, MatrixB, bias);
    std::vector<std::vector<double>> errors(RowsA, std::vector<double>(ColumnsB, 0.0));
    std::vector<std::vector<double>> updated_weights(ColumnsA, std::vector<double>(ColumnsB, 0.0));

    do {
        double AbsoluteError = 0.0;
        double derivative_bias = 0.0;

        for (int i = 0; i < RowsA; i++) {
            errors[i][0] = predictions[i][0] - VectorSolubility[i][0];
            AbsoluteError += std::abs(errors[i][0]);
        }

        MeanError = AbsoluteError / RowsA;

        std::cout << "Epoch " << epoch << " | MAE: " << MeanError << std::endl;

        if (std::isnan(MeanError) || std::isinf(MeanError) || MeanError > 1e6) {
            std::cout << "ERROR: Divergence detected! Stopping training." << std::endl;
            break;
        }

        for (int i = 0; i < ColumnsA; i++) {
            double current_term = 0.0;
            for (int j = 0; j < RowsA; j++) {
                current_term += (MatrixA[j][i] * errors[j][0]);
            }
            current_term /= RowsA;
            updated_weights[i][0] = MatrixB[i][0] - (learning_rate * current_term);
        }

        for (int i = 0; i < RowsA; i++) {
            derivative_bias += errors[i][0];
        }
        derivative_bias /= RowsA;
        bias -= (learning_rate * derivative_bias);

        MatrixB = updated_weights;
        predictions = MatrixMultiplierWithBias(MatrixA, MatrixB, bias);
        epoch++;

    } while (MeanError > 0.01 && epoch < max_epochs);

    std::ofstream ChangedBias(bias_path.string());

    EditFile(weight_path.string(), MatrixB);
    EditFile(predictions_path.string(), predictions);

    if (ChangedBias.is_open()) {
        ChangedBias << bias << "\n";
        ChangedBias.close();
    }

    std::cout << "Finished training at epoch " << epoch << " with MAE: " << MeanError << std::endl;

    return 0;
}