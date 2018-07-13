#if INTERACTIVE
#r @"../bin/Liquid1.dll"
#else
namespace Microsoft.Research.Liquid
#endif

open System
open System.IO
open Microsoft.Research.Liquid
open Util
open Operations

module circfunc =

    type System.String with
        member s1.icompare(s2: string) =
            System.String.Equals(s1, s2, System.StringComparison.CurrentCultureIgnoreCase)

    let cRk (k:int, qs:Qubits) =
        let gate =
            let nam = "controlled Rk"
            new Gate(
                Mat = (
                    let phi = 2.*Math.PI/Math.Pow(2.,(float)k)
                    let elem_real = Math.Cos phi
                    let elem_imag = Math.Sin phi
                    CSMat(4,[(0,0,1.,0.);(1,1,1.,0.);(2,2,1.,0.);(3,3,elem_real,elem_imag)])
                ))
        gate.Run qs

    let Yb (qs:Qubits) =
        let gate =
            new Gate(
                Mat = (CSMat(2,[(0,0,0.,0.);(0,1,0.,1.);(1,0,0.,1.);(1,1,0.,0.)]))
                )
        gate.Run qs

    let Ybd (qs:Qubits) =
        let gate =
            new Gate(
                Mat = (CSMat(2,[(0,0,0.,0.);(0,1,0.,-1.);(1,0,0.,-1.);(1,1,0.,0.)]))
                )
        gate.Run qs

    let Rx (theta:double, qs:Qubits) =
        let gate =
            new Gate(
                Mat = (
                    let c = Math.Cos (theta/2.)
                    let s = Math.Sin (theta/2.)
                    CSMat(2,[(0,0,c,0.);(0,1,0.,-s);(1,0,0.,-s);(1,1,c,0.)])
            ))
        gate.Run qs

    let Ry (theta:double, qs:Qubits) =
        let gate =
            new Gate(
                Mat = (
                    let c = Math.Cos (theta/2.)
                    let s = Math.Sin (theta/2.)
                    CSMat(2,[(0,0,c,0.);(0,1,-s,0.);(1,0,s,0.);(1,1,c,0.)])
                ))
        gate.Run qs

    let Rz (theta:double, qs:Qubits) =
        let gate =
            new Gate(
                Mat = (
                    let c = Math.Cos (theta/2.)
                    let s = Math.Sin (theta/2.)
                    CSMat(2,[(0,0,c,-s);(0,1,0.,0.);(1,0,0.,0.);(1,1,c,s)])
                ))
        gate.Run qs

    type QubitTimer() =
        let sw  =
            let sw  = Diagnostics.Stopwatch()
            show ""
            show "%8s %8s %8s %s" "Secs/Op" "S/Qubit" "Mem(GB)" "Operation"
            show "%8s %8s %8s %s" "-------" "-------" "-------" "---------"
            sw.Restart()
            sw

        member x.Show(str:string,?i:int,?reset:bool) =
            let i           = defaultArg i 1
            let reset       = defaultArg reset true
            let ps          = procStats(false)
            let secs        = float sw.ElapsedMilliseconds / 1000.0
            let spi         = secs / float i
            show "%8.3f %8.3f %8.3f %s" secs spi (float ps.privMB / 1024.) str
            if reset then sw.Restart()

        member x.Time() =
            float sw.ElapsedMilliseconds / 1000.0


    [<LQD>]
    let runqasmcirc() =

        let qfunc0(qs:Qubits) =

            CNOT[qs.[5];qs.[2]]
        let qfunc1(qs:Qubits) =

            CNOT[qs.[0];qs.[1]]
            Rx(0.00650000, [qs.[3]])
            Rx(0.06620000, [qs.[4]])
        let qfunc2(qs:Qubits) =

            CNOT[qs.[5];qs.[4]]
            CNOT[qs.[3];qs.[0]]
            Rx(0.06560000, [qs.[1]])
        let qfunc3(qs:Qubits) =

            Rx(0.04990000, [qs.[2]])
            CNOT[qs.[0];qs.[2]]
            CNOT[qs.[1];qs.[3]]
        let qfunc4(qs:Qubits) =

            Rz(0.06570000, [qs.[4]])
            Rx(0.06370000, [qs.[5]])
            CNOT[qs.[4];qs.[5]]
        let qfunc5(qs:Qubits) =

            CNOT[qs.[0];qs.[1]]
            Rx(0.03580000, [qs.[2]])
            Rx(0.05870000, [qs.[3]])
        let qfunc6(qs:Qubits) =

            CNOT[qs.[2];qs.[5]]
            CNOT[qs.[1];qs.[0]]
            Rx(0.00610000, [qs.[3]])
        let qfunc7(qs:Qubits) =

            Rx(0.00390000, [qs.[4]])
            CNOT[qs.[2];qs.[3]]
            CNOT[qs.[4];qs.[1]]
        let qfunc8(qs:Qubits) =

            Rz(0.00490000, [qs.[0]])
            Rz(0.05290000, [qs.[5]])
            CNOT[qs.[1];qs.[0]]
        let qfunc9(qs:Qubits) =

            CNOT[qs.[2];qs.[3]]
            Rz(0.08450000, [qs.[4]])
            Rz(0.04060000, [qs.[5]])
        let qfunc10(qs:Qubits) =

            CNOT[qs.[2];qs.[4]]
            CNOT[qs.[1];qs.[0]]
            Rz(0.02730000, [qs.[3]])
        let qfunc11(qs:Qubits) =

            Rz(0.02470000, [qs.[5]])
            CNOT[qs.[2];qs.[1]]
            CNOT[qs.[5];qs.[3]]
        let qfunc12(qs:Qubits) =

            Rx(0.04890000, [qs.[0]])
            Rx(0.06500000, [qs.[4]])
            CNOT[qs.[2];qs.[3]]
        let qfunc13(qs:Qubits) =

            CNOT[qs.[1];qs.[4]]
            Rz(0.01380000, [qs.[0]])
            Rz(0.05630000, [qs.[5]])
        let Ntest = 1
        let Nops = 18000.0
        let kettest = Ket(Ntest)
        let qtest = kettest.Qubits
        let testfunc(qtest:Qubits) =
            for j = 1 to 9000 do
                H [qtest.[0]]
                Yb [qtest.[0]]
                Ybd [qtest.[0]]

        let circuittest = Circuit.Compile testfunc qtest
        let qttest = QubitTimer()
        circuittest.Run qtest
        let test_time = qttest.Time()
        qttest.Show "Benchmark time (non-trivial)"

        let testfunc0(qtest:Qubits) =
           H [qtest.[0]]
        let circuittest0 = Circuit.Compile testfunc0 qtest
        let qttest0 = QubitTimer()
        circuittest0.Run qtest
        let test_time0 = qttest0.Time()
        qttest0.Show "Benchmark time (trivial)"

        let Nqubits     = 6
        let ket     = Ket(Nqubits)
        let qs      = ket.Qubits
        let qt      = QubitTimer()
        let fns = [qfunc0;qfunc1;qfunc2;qfunc3;qfunc4;qfunc5;qfunc6;qfunc7;qfunc8;qfunc9;qfunc10;qfunc11;qfunc12;qfunc13]
        let circs   = List.map (fun f ->
                        let circ    = Circuit.Compile f qs
                        let circ    = circ.GrowGates ket
                        circ) fns
        let comp_time = qt.Time()
        qt.Show "Compile cost"
        for circ in circs do
            circ.Run qs
        let comp_runtime = qt.Time()
        qt.Show "Compiled circuit run time"

        // the full state vector
        let cv = ket.Single()
        cv.Dump()
        let dim = pown 2 Nqubits
        let mutable cvr = 0.0
        let mutable cvi = 0.0
        let mutable nnz = 0 // number of non-zero elements
        let mutable nz_inds = Array.create (pown 2 Nqubits) 0 // indices of non-zero elements
        let tol_drop = 1e-15
        for i=1 to dim do
            let ind = uint64(i-1)
            cvr <- (cv.rSafe ind)
            cvi <- (cv.iSafe ind)
            printfn "v(%d) = %4.12f+%4.12fi" (i-1) cvr cvi
            if (((abs cvr) > tol_drop) || ((abs cvi) > tol_drop)) then
                nz_inds.[nnz] <- i-1
                nnz <- nnz + 1

        // measurement string of pauli operators
        let measure_path = "tests/measureTestZI.txt"
        let readMeasureString = measure_path |> File.ReadAllLines |> Array.mapi (fun i line -> (i,line))
        let num, str = readMeasureString.[0]
        let sep = [|" "|]
        let str_split = str.Split(sep, System.StringSplitOptions.None)
        let mutable flip_cnt = 0
        let mutable array_pauli = Array.zeroCreate Nqubits
        let mutable array_flip = Array.zeroCreate Nqubits
        for i = 0 to Nqubits-1 do
            let c = str_split.[i]
            if (c.icompare("X") = true) then
                array_pauli.[i] <- 1
            if (c.icompare("Y") = true) then
                array_pauli.[i] <- 2
            if (c.icompare("Z") = true) then
                array_pauli.[i] <- 3
            if (c.icompare("T") = true) then
                array_pauli.[i] <- 0
            if ((c.icompare("X") = true) || (c.icompare("Y") = true)) then
                array_flip.[flip_cnt] <- i+1
                flip_cnt <- flip_cnt+1

        // helper functions for evaluating the expectation value of pauli string
        let dec2bin(i:int) =

            // convert i to binary
            let mutable i_bin = Array.create Nqubits 0
            let mutable i_iter = i
            for j = 0 to Nqubits-1 do
                i_bin.[Nqubits-1-j] <- (int(i_iter) % 2)
                i_iter <- i_iter - (int(i_iter) % 2)
                i_iter <- (int(i_iter) / 2)
            i_bin

        let index_map(i:int) =

            let i_bin = dec2bin(i)

            // flip the set of qubits determined by the measurement pauli string
            let mutable ind_set_flip = 0
            let mutable ind_flip = array_flip.[ind_set_flip]
            while (ind_flip > 0) do
                i_bin.[ind_flip-1] <- (1+(pown -1 (i_bin.[ind_flip-1]))) / 2
                ind_set_flip <- ind_set_flip + 1
                ind_flip <- array_flip.[ind_set_flip]

            // convert the binary form i_bin back to decimal
            let mutable out = 0
            for j = 0 to Nqubits-1 do
                out <- out + (pown 2 j) * i_bin.[Nqubits-1-j]
            out

        let complex_multiply(a:int[], b:int[]) =
            let mutable c = Array.create 2 0
            c.[0] <- a.[0]*b.[0] - a.[1]*b.[1]
            c.[1] <- a.[1]*b.[0] + a.[0]*b.[1]
            c

        let pauli_string_element(i_col:int) =
            let mutable out = Array.create 2 0 // output 2-tuple (real, imag)
            let mutable factor = Array.create 2 0
            out.[0] <- 1

            let i_bin = dec2bin(i_col)

            for j = 0 to Nqubits-1 do
                if (array_pauli.[j]=2) then
                    factor.[0] <- 0
                    factor.[1] <- (pown -1  (i_bin.[j]+1))
                    out <- complex_multiply(out, factor)
                    factor.[1] <- 0 // reset
                if (array_pauli.[j]=3) then
                    factor.[0] <- (pown -1 i_bin.[j])
                    factor.[1] <- 0
                    out <- complex_multiply(out, factor)
                    factor.[0] <- 0 // reset
            out

        let compute_expectation() =

            let mutable M_exp_real = 0.0 // the expectation value of M
            let mutable M_exp_imag = 0.0 // for debugging - should be 0 due to hermiticity

            // intermediate quantities
            let mutable cvr = 0.0
            let mutable cvi = 0.0
            let mutable cvr_map = 0.0
            let mutable cvi_map = 0.0
            let mutable M_elem = Array.create 2 0
            let mutable Mr = 0.0
            let mutable Mi = 0.0

            // loop indices
            let mutable j_col = 0
            let mutable j_row = 0
            let mutable ind = uint64(0)
            let mutable ind_map = uint64(0)

            for i_nnz = 0 to nnz-1 do

                j_row <- nz_inds.[i_nnz]
                j_col <- index_map(j_row)
                ind <- uint64(j_row)
                ind_map <- uint64(j_col)
                cvr <- (cv.rSafe ind)
                cvi <- (cv.iSafe ind)
                cvr_map <- (cv.rSafe ind_map)
                cvi_map <- (cv.iSafe ind_map)
                M_elem <- pauli_string_element(j_row)
                Mr <- float(M_elem.[0])
                Mi <- float(M_elem.[1])

                M_exp_real <- M_exp_real + (Mr*cvr+Mi*cvi)*cvr_map - (Mi*cvr-Mr*cvi)*cvi_map
                M_exp_imag <- M_exp_imag + (Mr*cvr+Mi*cvi)*cvi_map + (Mi*cvr-Mr*cvi)*cvr_map

            M_exp_real

        //////////////////////////////
        //       Run and Time       //
        //////////////////////////////

        let M_avg = compute_expectation()
        let exp_time = qt.Time()
        qt.Show "Compute expectation time"

        //////////////////////////////
        //       Output results     //
        //////////////////////////////

        let total_time = comp_time + comp_runtime + exp_time
        let total_ops = Nops * (comp_runtime - test_time0) / (test_time - test_time0)
        let filestr = [|(sprintf "%d" Nqubits);(sprintf "%4.4f" comp_time);(sprintf "%4.4f" total_time);(sprintf "%4.0f" total_ops);(sprintf "%4.24f" M_avg)|]
        File.WriteAllLines("out_time", filestr)

