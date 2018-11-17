figures:
	make figure3
	make figure4
	make figure5
	make figure6
	make figure7
	make table2

# MERA
figure3:
	python scripts/mera_treewidth_runtimes.py data/mera.csv plots/mera_treewidth_comparison

figure4:
	python scripts/mera_qubits.py data/mera.csv plots/mera_qubit_runtime

# qaoa
table2:
	python scripts/qaoa_treewidth_summary_table.py data/reduced_data.csv plots/qaoa_table.tex

figure5:
	python scripts/qaoa_treewidth_times.py data/qaoa.csv plots/qaoa_treewidth_times

figure6:
	python scripts/qaoa_run_time_vs_treewidth.py data/qaoa.csv plots/qaoa_run_time_vs_treewidth

figure7:
	python scripts/qaoa_simulation_times.py data/qaoa.csv plots/liquid_comparison
