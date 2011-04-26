#GraphViz Macro
This Macro shows how GraphViz generates an image graph from a dot file.


##Parameters
The body of the macro is the dot string definition of the graph which will generate a graph image.


## Example
We use the graphviz macro as follows:


###Sample 01
    <div class="macro macro_graphviz">
        digraph {

            node [    fill=cornflowerblue,
                      fontcolor=white,
                      shape=diamond,
                      style=filled];

            Step1 [   color=darkgoldenrod2,
                      fontcolor=navy,
                      label=start,
                      shape=box];

            Step2;

            Step3a [  style=filled,
                      fillcolor=grey80,
                      color=grey80,
                      shape=circle,
                      fontcolor=navy];

            Step1  -> Step2;
            Step1  -> Step2a;
            Step2a -> Step3a;
            Step3;
            Step3a -> Step3;
            Step3a -> Step2b;
            Step2  -> Step2b;
            Step2b -> Step3;

            End [ shape=rectangle,
                  color=darkgoldenrod2,
                  fontcolor=navy];

            Step3  -> End [label=193];
            }
    </div>


###Sample 02

    <div class="macro macro_graphviz">
        digraph finite_state_machine {

            rankdir=LR;
            size="8,5"
            node [shape = doublecircle]; LR_0 LR_3 LR_4 LR_8;
            node [shape = circle];
            LR_0 -> LR_2 [ label = "SS(B)" ];
            LR_0 -> LR_1 [ label = "SS(S)" ];
            LR_1 -> LR_3 [ label = "S($end)" ];
            LR_2 -> LR_6 [ label = "SS(b)" ];
            LR_2 -> LR_5 [ label = "SS(a)" ];
            LR_2 -> LR_4 [ label = "S(A)" ];
            LR_5 -> LR_7 [ label = "S(b)" ];
            LR_5 -> LR_5 [ label = "S(a)" ];
            LR_6 -> LR_6 [ label = "S(b)" ];
            LR_6 -> LR_5 [ label = "S(a)" ];
            LR_7 -> LR_8 [ label = "S(b)" ];
            LR_7 -> LR_5 [ label = "S(a)" ];
            LR_8 -> LR_6 [ label = "S(b)" ];
            LR_8 -> LR_5 [ label = "S(a)" ];
        }
    </div>


###Sample 01

<div class="macro macro_graphviz">
digraph {

  node [    fill=cornflowerblue,
            fontcolor=white,
            shape=diamond,
            style=filled];

  Step1 [   color=darkgoldenrod2,
            fontcolor=navy,
            label=start,
            shape=box];

  Step2;

  Step3a [  style=filled,
            fillcolor=grey80,
            color=grey80,
            shape=circle,
            fontcolor=navy];

  Step1  -> Step2;
  Step1  -> Step2a;
  Step2a -> Step3a;
  Step3;
  Step3a -> Step3;
  Step3a -> Step2b;
  Step2  -> Step2b;
  Step2b -> Step3;
  End [ shape=rectangle,
        color=darkgoldenrod2,
        fontcolor=navy];
  Step3  -> End [label=193];
}
</div>


###Sample 02

<div class="macro macro_graphviz">
digraph finite_state_machine {
    rankdir=LR;
    size="8,5"
    node [shape = doublecircle]; LR_0 LR_3 LR_4 LR_8;
    node [shape = circle];
    LR_0 -> LR_2 [ label = "SS(B)" ];
    LR_0 -> LR_1 [ label = "SS(S)" ];
    LR_1 -> LR_3 [ label = "S($end)" ];
    LR_2 -> LR_6 [ label = "SS(b)" ];
    LR_2 -> LR_5 [ label = "SS(a)" ];
    LR_2 -> LR_4 [ label = "S(A)" ];
    LR_5 -> LR_7 [ label = "S(b)" ];
    LR_5 -> LR_5 [ label = "S(a)" ];
    LR_6 -> LR_6 [ label = "S(b)" ];
    LR_6 -> LR_5 [ label = "S(a)" ];
    LR_7 -> LR_8 [ label = "S(b)" ];
    LR_7 -> LR_5 [ label = "S(a)" ];
    LR_8 -> LR_6 [ label = "S(b)" ];
    LR_8 -> LR_5 [ label = "S(a)" ];
}
</div>
