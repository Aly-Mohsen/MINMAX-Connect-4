#import igraph
from igraph import *
import plotly.graph_objects as go

def make_annotations(pos, M, text, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=text[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations


def plot_tree(depth, children, text):

    sum=0
    for i in range(depth+1):
        sum+=children**i
    
    if(len(text)<sum):
        sum=len(text)

    nr_vertices = sum      #Number of total nodes = 7^depth*2 -1
    v_label = list(map(str, range(nr_vertices)))
    G = Graph.Tree(nr_vertices,children) # 7 stands for children number
    lay = G.layout('rt')
    lay = G.layout_reingold_tilford(mode="in", root=0)


    #Delete vertices that are None
    # count=0
    # none_vertex = []
    # vertex=[]
    # for i in range(0, len(text)) :
    #     if text[i] == 'None' :
    #         none_vertex.append(i)
    #         count+=1
    #     else:
    #         vertex.append(i)
    
    # nr_vertices= nr_vertices - count

    # while(count):
    #     text.remove('None')
    #     count-=1

    # #G = G.subgraph(vertex)
    # #G.delete_vertices(none_vertex)
    # G=induced_subgraph()

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G) # sequence of edges
    E = [e.tuple for e in G.es] # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

    labels = v_label


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                    y=Ye,
                    mode='lines',
                    line=dict(color='rgb(210,210,210)', width=1),
                    hoverinfo='none'
                    ))
    fig.add_trace(go.Scatter(x=Xn,
                    y=Yn,
                    mode='markers',
                    name='bla',
                    marker=dict(symbol='circle-dot',
                                    size=18,
                                    color='#6175c1',    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=1)
                                    ),
                    text=text,
                    hoverinfo='text',
                    opacity=0.8
                    ))



    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    fig.update_layout(title= 'Minimax Tree',
                annotations=make_annotations(position, M, text),  #replace v_labels with text
                font_size=12,
                showlegend=False,
                xaxis=axis,
                yaxis=axis,
                margin=dict(l=40, r=40, b=85, t=100),
                hovermode='closest',
                plot_bgcolor='rgb(248,248,248)'
                )

    fig.show()