#!/usr/bin/env python3
"""
AI Integration Framework for gUFO-Enhanced ICAC Ontology
=======================================================

Demonstrates advanced AI/ML capabilities leveraging gUFO foundational
ontology concepts for ICAC investigation analytics and prediction.

Features:
- Investigation efficiency prediction
- Role conflict detection
- Temporal pattern analysis
- Risk assessment
- Outcome prediction
"""

import rdflib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, regression_report
import networkx as nx
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class gUFOInvestigationAnalytics:
    """Advanced analytics for gUFO-enhanced ICAC investigations"""
    
    def __init__(self, ontology_path, endpoint_url=None):
        """Initialize analytics framework
        
        Args:
            ontology_path: Path to gUFO-enhanced ICAC ontology
            endpoint_url: SPARQL endpoint URL (optional)
        """
        self.graph = rdflib.Graph()
        self.graph.parse(ontology_path, format='turtle')
        self.endpoint_url = endpoint_url
        
        # ML models
        self.efficiency_model = None
        self.risk_model = None
        self.outcome_model = None
        
        # Scalers and encoders
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
        print(f"✅ Loaded gUFO-enhanced ICAC ontology: {len(self.graph)} triples")
    
    def extract_investigation_features(self):
        """Extract ML features from gUFO-enhanced investigation data"""
        
        query = """
        PREFIX icac-gufo: <https://ontology.unifiedcyberontology.org/icac/gufo#>
        PREFIX icac-temporal: <https://ontology.unifiedcyberontology.org/icac/temporal#>
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?investigation ?phase_count ?role_count ?event_count 
               ?urgency ?duration_days ?suspension_count ?efficiency WHERE {
            
            ?investigation rdf:type icac-gufo:Investigation ;
                          icac-temporal:urgencyLevel ?urgency ;
                          icac-temporal:hasTimeToResolution ?duration .
            
            # Count phases
            {
                SELECT ?investigation (COUNT(?phase) as ?phase_count) WHERE {
                    ?investigation icac-gufo:hasPhase ?phase .
                } GROUP BY ?investigation
            }
            
            # Count roles
            {
                SELECT ?investigation (COUNT(?role) as ?role_count) WHERE {
                    ?investigation icac-gufo:hasRole ?role .
                } GROUP BY ?investigation
            }
            
            # Count events
            {
                SELECT ?investigation (COUNT(?event) as ?event_count) WHERE {
                    ?event icac-gufo:participatesInInvestigation ?investigation .
                } GROUP BY ?investigation
            }
            
            # Count suspensions
            {
                SELECT ?investigation (COUNT(?suspension) as ?suspension_count) WHERE {
                    ?suspension rdf:type icac-temporal:SuspensionEvent ;
                               icac-temporal:suspends ?investigation .
                } GROUP BY ?investigation
            }
            
            # Get efficiency from phases
            OPTIONAL {
                ?investigation icac-gufo:hasPhase ?phase .
                ?phase icac-temporal:phaseEfficiency ?efficiency .
            }
            
            # Convert duration to days
            BIND(xsd:decimal(REPLACE(REPLACE(STR(?duration), "P", ""), "D.*", "")) as ?duration_days)
        }
        """
        
        results = list(self.graph.query(query))
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'investigation_id': str(row.investigation),
            'phase_count': int(row.phase_count),
            'role_count': int(row.role_count), 
            'event_count': int(row.event_count),
            'urgency_level': int(row.urgency),
            'duration_days': float(row.duration_days) if row.duration_days else 0,
            'suspension_count': int(row.suspension_count),
            'efficiency': float(row.efficiency) if row.efficiency else 1.0
        } for row in results])
        
        print(f"📊 Extracted features for {len(df)} investigations")
        return df
    
    def train_efficiency_predictor(self, df):
        """Train investigation efficiency prediction model"""
        
        # Features for efficiency prediction
        feature_cols = ['phase_count', 'role_count', 'event_count', 
                       'urgency_level', 'suspension_count', 'duration_days']
        
        X = df[feature_cols].fillna(0)
        y = df['efficiency'].fillna(1.0)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.efficiency_model = GradientBoostingRegressor(
            n_estimators=100, random_state=42
        )
        self.efficiency_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.efficiency_model.score(X_train_scaled, y_train)
        test_score = self.efficiency_model.score(X_test_scaled, y_test)
        
        print(f"🎯 Efficiency Predictor - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
        
        # Feature importance
        importance = self.efficiency_model.feature_importances_
        for i, feature in enumerate(feature_cols):
            print(f"   {feature}: {importance[i]:.3f}")
        
        return self.efficiency_model
    
    def predict_investigation_efficiency(self, investigation_features):
        """Predict investigation efficiency for new case"""
        
        if self.efficiency_model is None:
            raise ValueError("Efficiency model not trained. Call train_efficiency_predictor() first.")
        
        features_scaled = self.scaler.transform([investigation_features])
        efficiency = self.efficiency_model.predict(features_scaled)[0]
        
        return {
            'predicted_efficiency': efficiency,
            'efficiency_category': self._categorize_efficiency(efficiency),
            'confidence': self.efficiency_model.score(features_scaled.reshape(1, -1), [efficiency])
        }
    
    def detect_role_conflicts(self):
        """Detect potential role conflicts using gUFO role semantics"""
        
        query = """
        PREFIX icac-gufo: <https://ontology.unifiedcyberontology.org/icac/gufo#>
        
        SELECT ?person ?role1 ?role2 ?investigation ?conflict_type WHERE {
            ?person icac-gufo:playsRole ?role1 ;
                   icac-gufo:playsRole ?role2 .
            
            ?role1 icac-gufo:participatesInInvestigation ?investigation .
            ?role2 icac-gufo:participatesInInvestigation ?investigation .
            
            # Different roles for same person in same investigation
            FILTER(?role1 != ?role2)
            
            # Check for specific conflict types
            BIND(
                IF((?role1 = icac-gufo:VictimRole && ?role2 = icac-gufo:OffenderRole) ||
                   (?role1 = icac-gufo:OffenderRole && ?role2 = icac-gufo:VictimRole),
                   "VICTIM-OFFENDER-CONFLICT",
                IF((?role1 = icac-gufo:InvestigatorRole && ?role2 = icac-gufo:OffenderRole) ||
                   (?role1 = icac-gufo:OffenderRole && ?role2 = icac-gufo:InvestigatorRole),
                   "INVESTIGATOR-OFFENDER-CONFLICT",
                   "ROLE-OVERLAP")) as ?conflict_type
            )
        }
        """
        
        results = list(self.graph.query(query))
        
        conflicts = []
        for row in results:
            conflicts.append({
                'person': str(row.person),
                'role1': str(row.role1),
                'role2': str(row.role2),
                'investigation': str(row.investigation),
                'conflict_type': str(row.conflict_type),
                'severity': 'CRITICAL' if 'CONFLICT' in str(row.conflict_type) else 'WARNING'
            })
        
        print(f"⚠️  Detected {len(conflicts)} role conflicts")
        return conflicts
    
    def analyze_temporal_patterns(self):
        """Analyze temporal patterns using gUFO temporal framework"""
        
        query = """
        PREFIX icac-temporal: <https://ontology.unifiedcyberontology.org/icac/temporal#>
        PREFIX icac-gufo: <https://ontology.unifiedcyberontology.org/icac/gufo#>
        PREFIX gufo: <http://purl.org/nemo/gufo#>
        
        SELECT ?investigation ?phase_type ?duration_hours ?efficiency ?urgency WHERE {
            ?investigation rdf:type icac-gufo:Investigation ;
                          icac-temporal:urgencyLevel ?urgency ;
                          icac-gufo:hasPhase ?phase .
            
            ?phase rdf:type ?phase_type ;
                   icac-gufo:phaseDuration ?duration ;
                   icac-temporal:phaseEfficiency ?efficiency .
            
            # Convert duration to hours
            BIND(
                IF(CONTAINS(STR(?duration), "PT"),
                   xsd:decimal(REPLACE(REPLACE(STR(?duration), "PT", ""), "H.*", "")),
                   xsd:decimal(REPLACE(REPLACE(STR(?duration), "P", ""), "D.*", "")) * 24
                ) as ?duration_hours
            )
        }
        """
        
        results = list(self.graph.query(query))
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([{
            'investigation': str(row.investigation),
            'phase_type': str(row.phase_type).split('#')[-1],
            'duration_hours': float(row.duration_hours),
            'efficiency': float(row.efficiency),
            'urgency': int(row.urgency)
        } for row in results])
        
        # Temporal pattern analysis
        patterns = {
            'phase_efficiency': df.groupby('phase_type')['efficiency'].agg(['mean', 'std']),
            'urgency_impact': df.groupby('urgency')['duration_hours'].agg(['mean', 'count']),
            'efficiency_correlation': df[['duration_hours', 'efficiency', 'urgency']].corr()
        }
        
        print("📅 Temporal Pattern Analysis:")
        print("Phase Efficiency by Type:")
        print(patterns['phase_efficiency'])
        print("\nUrgency Impact on Duration:")
        print(patterns['urgency_impact'])
        
        return patterns
    
    def build_investigation_network(self):
        """Build network graph of investigation relationships using gUFO"""
        
        query = """
        PREFIX icac-gufo: <https://ontology.unifiedcyberontology.org/icac/gufo#>
        PREFIX icac-temporal: <https://ontology.unifiedcyberontology.org/icac/temporal#>
        
        SELECT ?investigation ?person ?role ?event WHERE {
            ?investigation rdf:type icac-gufo:Investigation .
            
            # Person-Investigation connections via roles
            OPTIONAL {
                ?investigation icac-gufo:hasRole ?role .
                ?person icac-gufo:playsRole ?role .
            }
            
            # Event-Investigation connections
            OPTIONAL {
                ?event icac-gufo:participatesInInvestigation ?investigation .
            }
        }
        """
        
        results = list(self.graph.query(query))
        
        # Build NetworkX graph
        G = nx.Graph()
        
        for row in results:
            inv = str(row.investigation)
            
            # Add investigation node
            G.add_node(inv, type='investigation')
            
            # Add person nodes and edges
            if row.person:
                person = str(row.person)
                role = str(row.role)
                G.add_node(person, type='person')
                G.add_edge(inv, person, relationship='role', role_type=role)
            
            # Add event nodes and edges
            if row.event:
                event = str(row.event)
                G.add_node(event, type='event')
                G.add_edge(inv, event, relationship='participation')
        
        print(f"🕸️  Built investigation network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        # Network analysis
        analysis = {
            'centrality': nx.degree_centrality(G),
            'clustering': nx.clustering(G),
            'components': list(nx.connected_components(G))
        }
        
        return G, analysis
    
    def predict_investigation_risk(self, df):
        """Predict investigation risk levels using gUFO features"""
        
        # Create risk labels based on efficiency and urgency
        def create_risk_label(row):
            if row['urgency_level'] >= 4 and row['efficiency'] < 0.8:
                return 'HIGH'
            elif row['urgency_level'] >= 3 and row['efficiency'] < 0.9:
                return 'MEDIUM'
            else:
                return 'LOW'
        
        df['risk_level'] = df.apply(create_risk_label, axis=1)
        
        # Features for risk prediction
        feature_cols = ['phase_count', 'role_count', 'event_count', 
                       'urgency_level', 'suspension_count']
        
        X = df[feature_cols].fillna(0)
        y = df['risk_level']
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train model
        self.risk_model = RandomForestClassifier(
            n_estimators=100, random_state=42
        )
        self.risk_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.risk_model.predict(X_test)
        
        print("🎯 Risk Prediction Model Performance:")
        print(classification_report(y_test, y_pred, 
                                  target_names=self.label_encoder.classes_))
        
        return self.risk_model
    
    def generate_investigation_insights(self, df):
        """Generate actionable insights from gUFO-enhanced data"""
        
        insights = {
            'efficiency_bottlenecks': [],
            'risk_factors': [],
            'optimization_opportunities': [],
            'resource_allocation': []
        }
        
        # Efficiency bottlenecks
        low_efficiency = df[df['efficiency'] < 0.7]
        if not low_efficiency.empty:
            insights['efficiency_bottlenecks'] = [
                f"Found {len(low_efficiency)} investigations with efficiency < 70%",
                f"Average suspension count in low-efficiency cases: {low_efficiency['suspension_count'].mean():.1f}",
                f"Most common phase count in bottlenecks: {low_efficiency['phase_count'].mode().iloc[0]}"
            ]
        
        # Risk factors
        high_risk = df[df['urgency_level'] >= 4]
        if not high_risk.empty:
            insights['risk_factors'] = [
                f"High urgency cases (level 4+): {len(high_risk)} ({len(high_risk)/len(df)*100:.1f}%)",
                f"Average resolution time for high urgency: {high_risk['duration_days'].mean():.1f} days",
                f"Role complexity in high-risk cases: {high_risk['role_count'].mean():.1f} roles"
            ]
        
        # Optimization opportunities
        suspended_cases = df[df['suspension_count'] > 0]
        if not suspended_cases.empty:
            insights['optimization_opportunities'] = [
                f"Cases with suspensions: {len(suspended_cases)} ({len(suspended_cases)/len(df)*100:.1f}%)",
                f"Potential time savings if suspensions reduced by 50%",
                f"Focus on cases with {suspended_cases['suspension_count'].max()} or more suspensions"
            ]
        
        # Resource allocation
        insights['resource_allocation'] = [
            f"Average roles per investigation: {df['role_count'].mean():.1f}",
            f"Average events per investigation: {df['event_count'].mean():.1f}",
            f"Recommended staffing for efficiency > 90%: {df[df['efficiency'] > 0.9]['role_count'].mean():.1f} roles"
        ]
        
        return insights
    
    def _categorize_efficiency(self, efficiency):
        """Categorize efficiency score"""
        if efficiency >= 1.2:
            return "VERY_HIGH"
        elif efficiency >= 1.0:
            return "HIGH"
        elif efficiency >= 0.8:
            return "MEDIUM"
        else:
            return "LOW"

def main():
    """Demonstrate AI integration with gUFO-enhanced ICAC ontology"""
    
    print("🚀 gUFO-Enhanced ICAC Investigation Analytics")
    print("=" * 50)
    
    # Initialize analytics framework
    analytics = gUFOInvestigationAnalytics('icac-core-gufo.ttl')
    
    # Extract features from gUFO-enhanced data
    df = analytics.extract_investigation_features()
    
    if len(df) > 0:
        print("\n📊 Training ML Models...")
        
        # Train efficiency predictor
        analytics.train_efficiency_predictor(df)
        
        # Train risk predictor
        analytics.train_risk_predictor(df)
        
        print("\n🔍 Analyzing Patterns...")
        
        # Detect role conflicts
        conflicts = analytics.detect_role_conflicts()
        
        # Analyze temporal patterns
        patterns = analytics.analyze_temporal_patterns()
        
        # Build investigation network
        network, network_analysis = analytics.build_investigation_network()
        
        # Generate insights
        insights = analytics.generate_investigation_insights(df)
        
        print("\n💡 Key Insights:")
        for category, insight_list in insights.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            for insight in insight_list:
                print(f"  • {insight}")
        
        print("\n✅ AI Integration Complete!")
        print("🎯 Enhanced capabilities now available for:")
        print("  • Investigation efficiency prediction")
        print("  • Role conflict detection")
        print("  • Temporal pattern analysis")
        print("  • Risk assessment")
        print("  • Network analysis")
        
    else:
        print("⚠️  No investigation data found. Load example data first.")

if __name__ == "__main__":
    main() 