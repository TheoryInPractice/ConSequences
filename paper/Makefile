provided_figures:
	make provided_figure3
	make provided_figure4
	make provided_figure5
	make provided_figure6
	make provided_figure7
	make provided_table2

# MERA
provided_figure3:
	python scripts/mera_treewidth_runtimes.py data/provided_mera.csv plots/mera_treewidth_comparison

provided_figure4:
	python scripts/mera_qubits.py data/provided_mera.csv plots/mera_qubit_runtime

# qTorch
provided_table2:
	python scripts/qtorch_treewidth_summary_table.py data/reduced_data.csv plots/qtorch_table.tex

provided_figure5:
	python scripts/qtorch_treewidth_times.py data/provided_qtorch.csv plots/qtorch_treewidth_times

provided_figure6:
	python scripts/qtorch_run_time_vs_treewidth.py data/provided_qtorch.csv plots/qtorch_run_time_vs_treewidth

provided_figure7:
	python scripts/qtorch_simulation_times.py data/provided_qtorch.csv plots/liquid_comparison
