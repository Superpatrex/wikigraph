import React, { useRef, useEffect, useState, useMemo, useCallback } from "react";
import ForceGraph3D from "react-force-graph-3d";
import * as THREE from 'three';
import { NODES, EDGES } from './constants.js';
import './App.css';

// Method that generates the graph data
const generateGraphData = () => {
  const nodes = NODES;
  const links = EDGES;
  return { nodes, links };
};

// Main App component
const App = () => {
  const tooltipRef = useRef();
  const graphRef = useRef();
  const [hoveredNode, setHoveredNode] = useState(null);

  // Generate the graph data
  const graphData = useMemo(() => generateGraphData(), []);

  // Method that handles the hover event on a node
  const handleNodeHover = (node) => {
    setHoveredNode(node);
    if (node) {
      const partitionString = getParititionString(node.partition);
      tooltipRef.current.style.display = "block";
      tooltipRef.current.innerHTML = `
        <strong>${node.name}</strong><br/>
        <em>ID:</em> ${node.id}<br/>
        <em>Partition:</em> ${partitionString}<br/>
        <em>Total Edges:</em> ${node.num_edges}<br/>
        <em>Bruh </br>
        <em>Rank:</em> ${node.rank}<br/>
        <em>PageRank:</em> ${node.page_rank}<br/>
        <em>Hubs:</em> ${node.hubs}<br/>
        <em>Authorities:</em> ${node.authorities}<br/>
      `;
    } 
    else 
    {
      tooltipRef.current.style.display = "none";
    }
  };

  // Method that returns the partition string based on the partition number
  const getParititionString = (partition) => {
    switch (partition) {
      case 0: return "Nixon Era";
      case 6: return "H. W. Bush/Clinton Era";
      case 4: return "Carter/Reagan Era";
      case 5: return "Bush Era";
      case 1: return "Obama Era";
      case 2: return "Trump Era";
      case 3: return "Biden Era";
      default: return "Unknown Era";
    }
  };

  // Method that opens the node's URL in a new tab
  const handleNodeClick = useCallback((node) => {
    if (node && node.url) {
      window.open(node.url, '_blank');
    }
  }, []);

  // Method that interpolates the color based on the partition of the node for the legend
  const interpolateColor = (partition) => {
    switch (partition) {
      case 0: return 0xFFB3B3;
      case 1: return 0xB3FFB3;
      case 2: return 0xB3B3FF;
      case 3: return 0xFFD9B3;
      case 4: return 0xFFB3DE;
      case 5: return 0xB3FFFF;
      case 6: return 0xFFFFB3;
      default: return 0xFFFFFF;
    }
  };

  // Method that creates the 3D object for each node
  const nodeThreeObject = useCallback((node) => {
    const minSize = 0; 
    const maxSize = 300;
    
    const color = interpolateColor(node.partition);
    
    // Create a sphere geometry for the node and set the size based on the number of edges
    const geometry = !node.is_president
      ? new THREE.SphereGeometry(Math.log2(node.size))
      : new THREE.SphereGeometry(Math.log2(node.size) * 2);
    
    // Create a material for the node
    const material =  new THREE.MeshBasicMaterial({ color });
    
    // Return the mesh object
    return new THREE.Mesh(geometry, material);
  }, []);

  // Method that changes the color of the link based on the hovered node
  const linkColor = useCallback((link) => 
  {
    if (hoveredNode && (link.source.id === hoveredNode.id || link.target.id === hoveredNode.id)) 
    {
      return 'rgba(255, 255, 255, 1.0)';
    }
    return 'rgba(255, 255, 255, 0.5)';
  }, [hoveredNode]);

  // Method that zooms the graph to fit the screen
  useEffect(() => {
    if (graphRef.current) {
      graphRef.current.zoomToFit(400);
    }
  }, []);

  // Render the graph
  return (
    <div style={{ position: "relative" }}>
      <div
        ref={tooltipRef}
        style={{
          position: "absolute",
          top: "10px",
          right: "10px",
          background: "rgba(255, 255, 255, 0.9)",
          padding: "10px",
          border: "1px solid #ccc",
          borderRadius: "5px",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          pointerEvents: "none",
          display: "none",
        }}
      ></div>
      <ForceGraph3D
        ref={graphRef}
        graphData={graphData}
        onNodeHover={handleNodeHover}
        onNodeClick={handleNodeClick}
        nodeLabel={(node) => 
          `<div class="tooltip-text">
            <strong>${node.name}</strong><br/>
            <em>ID:</em> ${node.id}<br/>
            <em>Partition:</em> ${getParititionString(node.partition)}<br/>
            <em>Total Edges:</em> ${node.num_edges}<br/>
            <em>PageRank:</em> ${node.page_rank}<br/>
            <em>PageRank Rank:</em> ${node.rank}<br/>
            <em>Betweenness Centrality:</em> ${node.betweenness_centrality}<br/>
            <em>Betweenness Centrality Rank:</em> ${node.betweenness_centrality_rank}<br/>
            <em>Closeness Centrality:</em> ${node.closeness_centrality}<br/>
            <em>Closeness Centrality Rank:</em> ${node.closeness_centrality_rank}<br/>
            <em>Eigenvector Centrality:</em> ${node.eigen_centrality}<br/>
            <em>Eigenvector Centrality Rank:</em> ${node.eigen_centrality_rank}<br/>
          </div>`}
        linkWidth={1}
        linkColor={linkColor}
        enableZoomInteraction
        enablePanInteraction
        cooldownTicks={0}
        warmupTicks={100}
        nodeResolution={1}
        nodeThreeObject={nodeThreeObject}
      />
      <div
        style={{
          position: "absolute",
          bottom: "20px",
          left: "20px",
          background: "rgba(0, 0, 0, 0.9)",
          padding: "20px",
          border: "1px solid #ccc",
          borderRadius: "5px",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          fontSize: "1.5em",
          color: "white",
        }}
      >
        <strong>Legend</strong><br/> 
        <span style={{ color: "#FFB3B3" }}>■</span> Nixon Era<br/>
        <span style={{ color: "#FFB3DE" }}>■</span> Carter/Reagan Era<br/>
        <span style={{ color: "#FFFFB3" }}>■</span> H. W. Bush/Clinton Era<br/>
        <span style={{ color: "#B3FFB3" }}>■</span> Bush Era<br/>
        <span style={{ color: "#B3FFFF" }}>■</span> Obama Era<br/>
        <span style={{ color: "#FFD9B3" }}>■</span> Biden Era<br/>
        <span style={{ color: "#B3B3FF" }}>■</span> Trump Era<br/>
      </div>
    </div>
    
  );
};

// Export the App component
export default React.memo(App);