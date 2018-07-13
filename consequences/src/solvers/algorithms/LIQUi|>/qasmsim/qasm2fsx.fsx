#if INTERACTIVE
#r @"../bin/Liquid1.dll"                 
#else
namespace Microsoft.Research.Liquid // Tell the compiler our namespace
#endif

open System                         // Open any support libraries
open System.IO
open Microsoft.Research.Liquid      // Get necessary Liquid libraries
open Util                           // General utilites
open Operations                     // Basic gates and operations

type System.String with
        member s1.icompare(s2: string) =
            System.String.Equals(s1, s2, System.StringComparison.CurrentCultureIgnoreCase)

let write_gate(gatename:string, angle:double, qubit1:int, qubit2:int) =
        let mutable str_out = [|""|]
        if (gatename.icompare("H") = true) then
            str_out <- [|(sprintf "            H [qs.[%d]]" qubit1)|]
        if (gatename.icompare("CNOT") = true) then
            str_out <- [|(sprintf "            CNOT[qs.[%d];qs.[%d]]" qubit1 qubit2)|]
        if (gatename.icompare("cRk") = true) then
            str_out <- [|(sprintf "            cRk(%d-%d+1,[qs.[%d];qs.[%d]])" qubit1 qubit2 qubit1 qubit2)|]
        if (gatename.icompare("Yb") = true || gatename.icompare("Hy") = true) then
            str_out <- [|(sprintf "            Yb [qs.[%d]]" qubit1)|]
        if (gatename.icompare("Ybd") = true || gatename.icompare("Hyh") = true) then
            str_out <- [|(sprintf "            Ybd [qs.[%d]]" qubit1)|]
        if (gatename.icompare("Rx") = true) then
            str_out <- [|(sprintf "            Rx(%4.8f, [qs.[%d]])" angle qubit1)|]
        if (gatename.icompare("Ry") = true) then
            str_out <- [|(sprintf "            Ry(%4.8f, [qs.[%d]])" angle qubit1)|]
        if (gatename.icompare("Rz") = true) then
            str_out <- [|(sprintf "            Rz(%4.8f, [qs.[%d]])" angle qubit1)|]
        str_out

let qasm2fsx(qasmfile_path:string, target_path:string, measure_path:string) =

    // generate header for the fsx file
    let mutable filestr = [|"#if INTERACTIVE";
                            @"#r @""../bin/Liquid1.dll""";               
                            "#else";
                            "namespace Microsoft.Research.Liquid"
                            "#endif";
                            "";
                            "open System";
                            "open System.IO";
                            "open Microsoft.Research.Liquid";
                            "open Util";
                            "open Operations";
                            ""|]
    
    // definitions for the gates
    filestr <- (Array.append filestr [|"module circfunc =";
                                       "";
                                       "    type System.String with";
                                       "        member s1.icompare(s2: string) =";
                                       "            System.String.Equals(s1, s2, System.StringComparison.CurrentCultureIgnoreCase)";
                                       "";
                                       "    let cRk (k:int, qs:Qubits) =";
                                       "        let gate =";
                                       @"            let nam = ""controlled Rk""";
                                       "            new Gate(";
                                       "                Mat = (";
                                       "                    let phi = 2.*Math.PI/Math.Pow(2.,(float)k)";
                                       "                    let elem_real = Math.Cos phi";
                                       "                    let elem_imag = Math.Sin phi";
                                       "                    CSMat(4,[(0,0,1.,0.);(1,1,1.,0.);(2,2,1.,0.);(3,3,elem_real,elem_imag)])";
                                       "                ))";
                                       "        gate.Run qs";
                                       "";
                                       "    let Yb (qs:Qubits) =";
                                       "        let gate =";
                                       "            new Gate(";
                                       "                Mat = (CSMat(2,[(0,0,0.,0.);(0,1,0.,1.);(1,0,0.,1.);(1,1,0.,0.)]))";
                                       "                )";
                                       "        gate.Run qs";
                                       "";
                                       "    let Ybd (qs:Qubits) =";
                                       "        let gate =";
                                       "            new Gate(";
                                       "                Mat = (CSMat(2,[(0,0,0.,0.);(0,1,0.,-1.);(1,0,0.,-1.);(1,1,0.,0.)]))";
                                       "                )";
                                       "        gate.Run qs";
                                       "";
                                       "    let Rx (theta:double, qs:Qubits) =";
                                       "        let gate =";
                                       "            new Gate(";
                                       "                Mat = (";
                                       "                    let c = Math.Cos (theta/2.)";
                                       "                    let s = Math.Sin (theta/2.)";
                                       "                    CSMat(2,[(0,0,c,0.);(0,1,0.,-s);(1,0,0.,-s);(1,1,c,0.)])";
                                       "            ))";
                                       "        gate.Run qs";
                                       "";
                                       "    let Ry (theta:double, qs:Qubits) =";
                                       "        let gate =";
                                       "            new Gate(";
                                       "                Mat = (";
                                       "                    let c = Math.Cos (theta/2.)";
                                       "                    let s = Math.Sin (theta/2.)";
                                       "                    CSMat(2,[(0,0,c,0.);(0,1,-s,0.);(1,0,s,0.);(1,1,c,0.)])";
                                       "                ))";
                                       "        gate.Run qs";
                                       "";
                                       "    let Rz (theta:double, qs:Qubits) =";
                                       "        let gate =";
                                       "            new Gate(";
                                       "                Mat = (";
                                       "                    let c = Math.Cos (theta/2.)";
                                       "                    let s = Math.Sin (theta/2.)";
                                       "                    CSMat(2,[(0,0,c,-s);(0,1,0.,0.);(1,0,0.,0.);(1,1,c,s)])";
                                       "                ))";
                                       "        gate.Run qs";
                                       ""|])

    // generate code for the qubit timer
    filestr <- (Array.append filestr [|"    type QubitTimer() =";
                                       "        let sw  =";
                                       "            let sw  = Diagnostics.Stopwatch()";
                                       @"            show """"";
                                       @"            show ""%8s %8s %8s %s"" ""Secs/Op"" ""S/Qubit"" ""Mem(GB)"" ""Operation""";
                                       @"            show ""%8s %8s %8s %s"" ""-------"" ""-------"" ""-------"" ""---------""";
                                       "            sw.Restart()";
                                       "            sw";
                                       "";
                                       "        member x.Show(str:string,?i:int,?reset:bool) =";
                                       "            let i           = defaultArg i 1";
                                       "            let reset       = defaultArg reset true";
                                       "            let ps          = procStats(false)";
                                       "            let secs        = float sw.ElapsedMilliseconds / 1000.0";
                                       "            let spi         = secs / float i";
                                       @"            show ""%8.3f %8.3f %8.3f %s"" secs spi (float ps.privMB / 1024.) str";
                                       "            if reset then sw.Restart()";
                                       "";
                                       "        member x.Time() =";
                                       "            float sw.ElapsedMilliseconds / 1000.0";
                                       ""|])

    // parsing .qasm files
    let readLines = qasmfile_path |> File.ReadAllLines |> Array.mapi (fun i line -> (i, line))
    let len_file = readLines.Length
    let max_index = len_file - 1
    let mutable Nqubits = 0
    let mutable c = '?' // first character of the line, initialized to '?'
    let mutable ket = Ket(Nqubits)
    let mutable qs = ket.Qubits

    let maxfuncsize = 2  // maximum number of lines per function built from .qasm commands (this restriction is necessary because mono allows a finite limit for stack size
    let mutable linectr = 0 // counter used during the parsing to enforce the maximum function size
    let mutable funcctr = 0 // counter used for marking the subroutines 
    let Ngates_benchmark = 9000 // number of Hadamard gates used for flop benchmark 

    // read through the .qasm file line by line and build an F# function
    filestr <- (Array.append filestr [|"";
                                       "    [<LQD>]";
                                       "    let runqasmcirc() =";
                                       "";|])

    // introduce the gate sequence as an F# function
    for i = 0 to max_index do
        if (linectr = 0) then 
            filestr <- (Array.append filestr [|(sprintf "        let qfunc%d(qs:Qubits) =" funcctr);""|])
            funcctr <- funcctr + 1
        let num, str = readLines.[i]
        if str.Length <> 0 then
            c <- str.[0]
            if (c.CompareTo('#') <> 0) then
                let sep = [|" "|]
                let str_split = str.Split(sep, System.StringSplitOptions.None)
                if (str_split.Length = 1) then
                    Nqubits <- Int32.Parse(str)
                    ket <- Ket(Nqubits)
                    qs <- ket.Qubits
                else
                    let gatename = str_split.[0]
                    let mutable qubit1 = -1
                    let mutable qubit2 = -1
                    let mutable angle = 0.0
                    if (gatename.icompare("Rx") = true || gatename.icompare("Ry") = true || gatename.icompare("Rz") = true) then
                        angle <- Double.Parse(str_split.[1])
                        qubit1 <- Int32.Parse(str_split.[2])
                    else
                        qubit1 <- Int32.Parse(str_split.[1])
                        if (str_split.Length = 3) then
                            qubit2 <- Int32.Parse(str_split.[2])
                    let mutable str_out = write_gate(gatename, angle, qubit1, qubit2)
                    filestr <- (Array.append filestr str_out)
        if (linectr = maxfuncsize) then
            linectr <- 0
        else 
            linectr <- linectr + 1  

    // non-trivial benchmark for counting flops
    let Nops_benchmark = 2 * Ngates_benchmark
    let max_gate_variety = 3
    let mutable gatectr = 0
    filestr <- (Array.append filestr [|"        let Ntest = 1";
                                       (sprintf "        let Nops = %d.0" Nops_benchmark);
                                       "        let kettest = Ket(Ntest)";
                                       "        let qtest = kettest.Qubits";
                                       "        let testfunc(qtest:Qubits) ="
                                       (sprintf "            for j = 1 to %d do" Ngates_benchmark);
                                       "                H [qtest.[0]]";
                                       "                Yb [qtest.[0]]";
                                       "                Ybd [qtest.[0]]";
                                       ""|])
    filestr <- (Array.append filestr [|"        let circuittest = Circuit.Compile testfunc qtest";
                                       "        let qttest = QubitTimer()";
                                       "        circuittest.Run qtest";
                                       "        let test_time = qttest.Time()";
                                       @"        qttest.Show ""Benchmark time (non-trivial)""";
                                       ""|])

    // trivial benchmark for determining the part of the time that is independent of number of gates
    filestr <- (Array.append filestr [|"        let testfunc0(qtest:Qubits) =";
                                       "           H [qtest.[0]]";
                                       "        let circuittest0 = Circuit.Compile testfunc0 qtest";
                                       "        let qttest0 = QubitTimer()";
                                       "        circuittest0.Run qtest";
                                       "        let test_time0 = qttest0.Time()";
                                       @"        qttest0.Show ""Benchmark time (trivial)""";
                                       ""|])

    // generate the code that compiles and runs the circuit
    let mutable string_fns = "        let fns = ["
    for i = 0 to funcctr-1 do
       string_fns <- string_fns + (sprintf "qfunc%d" i)
       if (i = funcctr-1) then 
           string_fns <- string_fns + "]"
       else
           string_fns <- string_fns + ";"  
    filestr <- (Array.append filestr [|(sprintf "        let Nqubits     = %d" Nqubits);
                                       "        let ket     = Ket(Nqubits)";
                                       "        let qs      = ket.Qubits";
                                       "        let qt      = QubitTimer()";
                                       string_fns;
                                       "        let circs   = List.map (fun f ->"; 
                                       "                        let circ    = Circuit.Compile f qs";
                                       "                        let circ    = circ.GrowGates ket";
                                       "                        circ) fns";
                                       "        let comp_time = qt.Time()"; 
                                       @"        qt.Show ""Compile cost""";
                                       "        for circ in circs do";
//                                       "            let cv_ = ket.Single()";
//                                       "            cv_.Dump()";
//                                       "            let dim_ = pown 2 Nqubits";
//                                       "            let mutable cvr_ = 0.0";
//                                       "            let mutable cvi_ = 0.0";
//                                       "            for i_ = 1 to dim_ do";
//                                       "                let ind_ = uint64(i_-1)";
//                                       "                cvr_ <- (cv_.rSafe ind_)";
//                                       "                cvi_ <- (cv_.iSafe ind_)";
//                                       @"                printfn ""v(%d) = %4.13f + %4.13fj"" (i_-1) cvr_ cvi_";
//                                       @"            printfn """"";
                                       "            circ.Run qs";
                                       "        let comp_runtime = qt.Time()";
                                       @"        qt.Show ""Compiled circuit run time""";
                                       ""|])

    // generate the code that computes the expectation value of measurement string
    filestr <- (Array.append filestr [|"        // the full state vector";
                                       "        let cv = ket.Single()";
                                       "        cv.Dump()";
                                       "        let dim = pown 2 Nqubits";
                                       "        let mutable cvr = 0.0";
                                       "        let mutable cvi = 0.0";
                                       "        let mutable nnz = 0 // number of non-zero elements";
                                       "        let mutable nz_inds = Array.create (pown 2 Nqubits) 0 // indices of non-zero elements";
                                       "        let tol_drop = 1e-15";
                                       "        for i=1 to dim do";
                                       "            let ind = uint64(i-1)";
                                       "            cvr <- (cv.rSafe ind)";
                                       "            cvi <- (cv.iSafe ind)";
                                       @"            printfn ""v(%d) = %4.12f+%4.12fi"" (i-1) cvr cvi";
                                       "            if (((abs cvr) > tol_drop) || ((abs cvi) > tol_drop)) then";
                                       "                nz_inds.[nnz] <- i-1";
                                       "                nnz <- nnz + 1";
                                       "";
                                       "        // measurement string of pauli operators";
                                       (sprintf @"        let measure_path = ""%s""" measure_path);
                                       "        let readMeasureString = measure_path |> File.ReadAllLines |> Array.mapi (fun i line -> (i,line))";
                                       "        let num, str = readMeasureString.[0]";
                                       @"        let sep = [|"" ""|]";
                                       "        let str_split = str.Split(sep, System.StringSplitOptions.None)";
                                       "        let mutable flip_cnt = 0";
                                       "        let mutable array_pauli = Array.zeroCreate Nqubits";
                                       "        let mutable array_flip = Array.zeroCreate Nqubits";
                                       "        for i = 0 to Nqubits-1 do";
                                       "            let c = str_split.[i]";
                                       @"            if (c.icompare(""X"") = true) then";
                                       "                array_pauli.[i] <- 1";
                                       @"            if (c.icompare(""Y"") = true) then";
                                       "                array_pauli.[i] <- 2";
                                       @"            if (c.icompare(""Z"") = true) then";
                                       "                array_pauli.[i] <- 3";
                                       @"            if (c.icompare(""T"") = true) then";
                                       "                array_pauli.[i] <- 0";
                                       @"            if ((c.icompare(""X"") = true) || (c.icompare(""Y"") = true)) then";
                                       "                array_flip.[flip_cnt] <- i+1";
                                       "                flip_cnt <- flip_cnt+1";
                                       "";
                                       "        // helper functions for evaluating the expectation value of pauli string";
                                       "        let dec2bin(i:int) =";
                                       "";
                                       "            // convert i to binary";
                                       "            let mutable i_bin = Array.create Nqubits 0";
                                       "            let mutable i_iter = i";
                                       "            for j = 0 to Nqubits-1 do";
                                       "                i_bin.[Nqubits-1-j] <- (int(i_iter) % 2)";
                                       "                i_iter <- i_iter - (int(i_iter) % 2)";
                                       "                i_iter <- (int(i_iter) / 2)";
                                       "            i_bin";
                                       "";
                                       "        let index_map(i:int) =";
                                       "";
                                       "            let i_bin = dec2bin(i)";
                                       "";
                                       "            // flip the set of qubits determined by the measurement pauli string";
                                       "            let mutable ind_set_flip = 0";
                                       "            let mutable ind_flip = array_flip.[ind_set_flip]";
                                       "            while (ind_flip > 0) do";
                                       "                i_bin.[ind_flip-1] <- (1+(pown -1 (i_bin.[ind_flip-1]))) / 2";
                                       "                ind_set_flip <- ind_set_flip + 1";
                                       "                ind_flip <- array_flip.[ind_set_flip]";
                                       "";
                                       "            // convert the binary form i_bin back to decimal";
                                       "            let mutable out = 0";
                                       "            for j = 0 to Nqubits-1 do";
                                       "                out <- out + (pown 2 j) * i_bin.[Nqubits-1-j]";
                                       "            out";
                                       "";
                                       "        let complex_multiply(a:int[], b:int[]) =";
                                       "            let mutable c = Array.create 2 0";
                                       "            c.[0] <- a.[0]*b.[0] - a.[1]*b.[1]";
                                       "            c.[1] <- a.[1]*b.[0] + a.[0]*b.[1]";
                                       "            c";
                                       "";
                                       "        let pauli_string_element(i_col:int) =";
                                       "            let mutable out = Array.create 2 0 // output 2-tuple (real, imag)";
                                       "            let mutable factor = Array.create 2 0";
                                       "            out.[0] <- 1";
                                       "";
                                       "            let i_bin = dec2bin(i_col)";
                                       "";
                                       "            for j = 0 to Nqubits-1 do";
                                       "                if (array_pauli.[j]=2) then";
                                       "                    factor.[0] <- 0";
                                       "                    factor.[1] <- (pown -1  (i_bin.[j]+1))";
                                       "                    out <- complex_multiply(out, factor)";
                                       "                    factor.[1] <- 0 // reset";
                                       "                if (array_pauli.[j]=3) then";
                                       "                    factor.[0] <- (pown -1 i_bin.[j])";
                                       "                    factor.[1] <- 0";
                                       "                    out <- complex_multiply(out, factor)";
                                       "                    factor.[0] <- 0 // reset";
                                       "            out";
                                       "";
                                       "        let compute_expectation() =";
                                       "";
                                       "            let mutable M_exp_real = 0.0 // the expectation value of M";
                                       "            let mutable M_exp_imag = 0.0 // for debugging - should be 0 due to hermiticity";
                                       "";
                                       "            // intermediate quantities";
                                       "            let mutable cvr = 0.0";
                                       "            let mutable cvi = 0.0";
                                       "            let mutable cvr_map = 0.0";
                                       "            let mutable cvi_map = 0.0";
                                       "            let mutable M_elem = Array.create 2 0";
                                       "            let mutable Mr = 0.0";
                                       "            let mutable Mi = 0.0";
                                       "";
                                       "            // loop indices";
                                       "            let mutable j_col = 0";
                                       "            let mutable j_row = 0";
                                       "            let mutable ind = uint64(0)";
                                       "            let mutable ind_map = uint64(0)";
                                       "";
                                       "            for i_nnz = 0 to nnz-1 do";
                                       "";
                                       "                j_row <- nz_inds.[i_nnz]";
                                       "                j_col <- index_map(j_row)";
                                       "                ind <- uint64(j_row)";
                                       "                ind_map <- uint64(j_col)";
                                       "                cvr <- (cv.rSafe ind)";
                                       "                cvi <- (cv.iSafe ind)";
                                       "                cvr_map <- (cv.rSafe ind_map)";
                                       "                cvi_map <- (cv.iSafe ind_map)";
                                       "                M_elem <- pauli_string_element(j_row)";
                                       "                Mr <- float(M_elem.[0])";
                                       "                Mi <- float(M_elem.[1])";
                                       "";
                                       "                M_exp_real <- M_exp_real + (Mr*cvr+Mi*cvi)*cvr_map - (Mi*cvr-Mr*cvi)*cvi_map";
                                       "                M_exp_imag <- M_exp_imag + (Mr*cvr+Mi*cvi)*cvi_map + (Mi*cvr-Mr*cvi)*cvr_map";
                                       "";
                                       "            M_exp_real";
                                       ""|])

    // generate the code for running and timing
    filestr <- (Array.append filestr [|"        //////////////////////////////";
                                       "        //       Run and Time       //";
                                       "        //////////////////////////////";
                                       ""|])
    filestr <- (Array.append filestr [|"        let M_avg = compute_expectation()";
                                       "        let exp_time = qt.Time()";
                                       @"        qt.Show ""Compute expectation time""";
                                       ""|])

    // generate the code that writes results to the file out_time
    filestr <- (Array.append filestr [|"        //////////////////////////////";
                                       "        //       Output results     //";
                                       "        //////////////////////////////";
                                       ""|])
    filestr <- (Array.append filestr [|"        let total_time = comp_time + comp_runtime + exp_time";
                                       "        let total_ops = Nops * (comp_runtime - test_time0) / (test_time - test_time0)";
                                       @"        let filestr = [|(sprintf ""%d"" Nqubits);(sprintf ""%4.4f"" comp_time);(sprintf ""%4.4f"" total_time);(sprintf ""%4.0f"" total_ops);(sprintf ""%4.24f"" M_avg)|]";
                                       @"        File.WriteAllLines(""out_time"", filestr)";
                                       ""|])

    // generate the line that calls and executes the entire function
//    filestr <- (Array.append filestr [|"circfunc.runqasmcirc"|])

    File.WriteAllLines(target_path,filestr)
    ()

let cmdline = Environment.GetCommandLineArgs()
printfn "source: %s\ntarget: %s\nmeasure: %s" cmdline.[3] cmdline.[4] cmdline.[5]
qasm2fsx(cmdline.[3], cmdline.[4], cmdline.[5])
